"""Schedule diary photos in Eden, for uploads where the shortcut said "Post to Eden: yes".

Reads the jobs diary_inbox.py wrote to $EDEN_JOBS and, per job, follows the Agent steps 6-10 of
vieren/sops/sop-photo-diary.md: wait until each photo is live, host it in Eden, take the first
free slot, schedule one post on the platforms the shortcut picked, then read it back.
"instagram-story" is not an Eden platform: it becomes one Story per photo, in the slots after the post.
A job with no "platforms" (an older shortcut) posts to DEFAULT.

Talks to Eden's MCP server (https://mcp.eden.so/mcp) with the API key in $EDEN_API_KEY as a
bearer token, the way Eden documents for Zapier. Stops with the raw error on any failure and never
publishes immediately.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

MCP = "https://mcp.eden.so/mcp"
SITE = "https://vieren.studio/"
DEFAULT = ["threads", "linkedin", "twitter", "substack", "facebook"]


class Eden:
    def __init__(self, key):
        self.key, self.session, self.n = key, None, 0

    def rpc(self, method, params=None, notify=False):
        body = {"jsonrpc": "2.0", "method": method, "params": params or {}}
        if not notify:
            self.n += 1
            body["id"] = self.n
        headers = {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json",
                   "Accept": "application/json, text/event-stream"}
        if self.session:
            headers["Mcp-Session-Id"] = self.session
        req = urllib.request.Request(MCP, json.dumps(body).encode(), headers)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                self.session = r.headers.get("Mcp-Session-Id") or self.session
                raw = r.read().decode()
        except urllib.error.HTTPError as e:
            sys.exit(f"Eden {method}: HTTP {e.code} {e.read().decode()[:500]}")
        if notify:
            return None
        # Streamable HTTP answers either with plain JSON or with SSE "data:" lines
        msgs = [json.loads(l[5:]) for l in raw.splitlines() if l.startswith("data:")] or [json.loads(raw)]
        msg = next(m for m in msgs if m.get("id") == body["id"])
        if "error" in msg:
            sys.exit(f"Eden {method}: {msg['error']}")
        return msg["result"]

    def tool(self, name, args):
        res = self.rpc("tools/call", {"name": name, "arguments": args})
        text = "".join(c.get("text", "") for c in res.get("content", []) if c.get("type") == "text")
        data = res.get("structuredContent") or json.loads(text)
        if res.get("isError") or not data.get("ok", False):
            sys.exit(f"Eden {name}: {text[:800]}")
        return data


def wait_live(url, minutes=10):
    for _ in range(minutes * 4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=20) as r:
                if r.status == 200:
                    return
        except urllib.error.URLError:
            pass
        time.sleep(15)
    sys.exit(f"not live after {minutes} min: {url}")


def segments_for(caption, media_ids):
    # Over 280 chars Eden auto-splits and drops the photo on X and Threads (SOP step 9): split ourselves
    cut = caption.rfind(" ", 0, 280)
    cut = cut if cut > 0 else 280
    return [{"text": caption[:cut].rstrip(), "mediaIds": media_ids}, {"text": caption[cut:].strip()}]


def main():
    jobs = [json.loads(l) for l in open(os.environ["EDEN_JOBS"]) if l.strip()]
    if not jobs:
        return
    key = os.environ.get("EDEN_API_KEY")
    if not key:
        sys.exit("Eden post asked for, but the EDEN_API_KEY repo secret is not set")
    eden = Eden(key)
    eden.rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                            "clientInfo": {"name": "vieren-diary-inbox", "version": "1"}})
    eden.rpc("notifications/initialized", notify=True)

    for job in jobs:
        photos = job["photos"][:6]  # Substack Notes reject more than 6 images
        if len(job["photos"]) > 6:
            print(f"{job['key']}: {len(job['photos'])} photos, only the first 6 go to Eden")
        media = []
        for path in photos:
            url = SITE + path
            wait_live(url)
            media.append(eden.tool("eden_import_scheduling_media", {"url": url})["asset"])
        ids = [m["id"] for m in media]
        picked = job.get("platforms") or DEFAULT
        feed = [p for p in picked if p != "instagram-story"]
        used = 0  # epoch of the last slot this job took
        if feed:
            sched, slot = free_slot(eden, used)
            args = {"scheduleId": sched["id"], "platforms": feed, "text": job["caption"], "media": media,
                    "scheduledFor": slot["epoch"], "idempotencyKey": job["key"]}
            if "twitter" in feed:
                args["perPlatform"] = {"twitter": {"mediaIds": ids[:4]}}
            if len(job["caption"]) > 280 and {"twitter", "threads"} & set(feed):
                args["segments"] = segments_for(job["caption"], ids[:4])
            report(eden, job["key"], eden.tool("eden_schedule_post", args), slot)
            used = slot["epoch"]
        if "instagram-story" in picked:
            # SOP step 9: one Story per photo, Instagram alone, exactly one image, next free slot each
            for i, m in enumerate(media, 1):
                sched, slot = free_slot(eden, used)
                args = {"scheduleId": sched["id"], "platforms": ["instagram"], "text": job["caption"],
                        "media": [m], "scheduledFor": slot["epoch"], "idempotencyKey": f"{job['key']}-story-{i}",
                        "perPlatform": {"instagram": {"story": True}}}
                report(eden, f"{job['key']}-story-{i}", eden.tool("eden_schedule_post", args), slot)
                used = slot["epoch"]


def free_slot(eden, after):
    # Re-read before every post; skip slots this job already took (UNTESTED whether Eden removes them)
    sched = next(s for s in eden.tool("eden_list_schedules", {})["schedules"] if s.get("isDefault"))
    slot = next((s for s in sched["nextFreeSlots"] if s["epoch"] > after), None)
    if not slot:
        sys.exit(f"no free Eden slot after {after}")
    return sched, slot


def report(eden, key, post, slot):
    check = eden.tool("eden_list_scheduled_posts", {"postId": post["id"], "mode": "full"})["posts"][0]
    states = {t["platform"]: t["status"] for t in check["targets"]}
    print(f"{key}: Eden post {post['id']} {check['status']} for {slot['dayLabel']} {slot['timeLabel']} {states}")


if __name__ == "__main__":
    main()
