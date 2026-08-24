---
title: "My Second Brain Gaslit Me for Months"
date: 2026-07-16
description: "I had the most sophisticated personal knowledge system of anyone I knew."
tags: []
draft: true
# imported from vieren/articles/drafts/2026-07-16-my-second-brain-gaslit-me-tucker.md
originalStatus: draft-tucker-v2
flavor: tucker
---

I had the most sophisticated personal knowledge system of anyone I knew.

An AI-powered digital brain that automatically organized my work, saved my ideas, backed up everything, and learned from every session I had with it. Six automated workers running around the clock. I wrote a viral thread about it (it's still in drafts). I was the guy with the second brain.

The second brain had been broken for weeks.

I did not know this.

## The Guy With the Second Brain

Let me set the stage so you understand how confident I was.

Every night at 2am, an automated worker would wake up, read every conversation I'd had with my AI that day, and file it into my permanent knowledge base. Automatically. While I slept. I'd wake up, open my vault, and yesterday's work would already be organized, connected to related notes, and stored for future reference.

That was one of six automated workers. One took a snapshot of the entire vault every five minutes and backed it up. One captured every message I sent from my phone and filed it. One pulled in research from the web. All of it humming in the background like a team of invisible assistants who never take a day off.

I told people about this setup with the energy of a man who had solved personal knowledge management forever.

I had not solved shit.

## Part One: The Feeling

For weeks, something felt wrong. The vault felt stale. Frozen. Like walking into your apartment and knowing someone's been in there, but nothing's obviously moved.

I'd check the reports. Green. Success. Done. Every timestamp current.

"You're imagining it," I told myself.

I was not imagining it.

## Part Two: Pulling the Thread

I finally stopped trusting the reports and looked at the actual vault. What I found over the next two hours aged me about five years.

**Discovery one.** The nightly memory worker had been clocking in on schedule. Every night, 2am, right on time. Its job: read yesterday's AI conversations, extract the important stuff, file it into long-term memory. The problem: the AI tool had moved where it stores conversations. Nobody told the worker. The worker didn't care. It showed up to the old address every night, found an empty room, filed nothing, and reported "done."

Imagine hiring a night-shift employee to sort your mail, and they show up every night to an empty mailbox because the post office changed your address. And every morning they hand you a report that says "all mail sorted." For weeks.

Not great.

**Discovery two.** The backup system. Taking a snapshot of my vault every five minutes, like clockwork. Beautiful, disciplined, consistent. I'd assumed it was also uploading those snapshots to the cloud. It was not. The upload had been silently failing since I changed a credential and forgot this system existed. 2,451 snapshots. Sitting on my laptop. Backed up nowhere.

Two thousand four hundred and fifty-one saves. On one machine. Like writing a novel in a house with no fire insurance and feeling safe because you hit save a lot.

Worse.

**Discovery three.** Two more automated workers I'd set up were assigned to tasks that no longer existed. I'd reorganized things during a cleanup, forgot to update their assignments. They'd been showing up to work every day, failing immediately, writing an error into a report nobody reads, and clocking out. Every day. For weeks.

"How long has this been happening?"

I checked the reports.

Weeks.

**Discovery four.** The vault had ballooned to 14GB. For context, a vault of text notes should be maybe a few hundred megabytes. Mine was fourteen gigabytes. The five-minute snapshots had been faithfully saving everything, including massive video files I'd pulled in for research and never cleaned up. The backup system never forgets. Every video, every frame, stored forever in the history, compounding every five minutes.

Fourteen. Gigabytes. Of what should be a folder of text files.

I actually laughed. What else can you do.

**Discovery five.** This is the one where I stopped laughing. The save-everything habit had swept private credentials into the backup history. A master database access code. Service credentials. And one, my personal favorite, sitting in plain text in the worker schedule itself. Just chilling there. Visible to anything that could read the schedule.

Like writing your banking PIN on the outside of your front door and feeling safe because nobody's mentioned it.

I built the most automated knowledge system I could imagine and it was leaking private access codes while reporting that everything was fine.

## The Diagnosis

Five failures. Five different symptoms. I wanted there to be five different causes because that would mean five isolated mistakes. Bad luck. Random stuff breaking.

There was one cause.

Every worker was allowed to claim "done" without proving it. "I ran" was treated as "I worked." The memory worker didn't check whether it actually found anything to file. The backup didn't check whether the upload went through. The other workers didn't check whether their assignments still existed. Every single automation I'd built just trusted itself.

The system that's supposed to remember everything had no memory of whether it itself was working.

I'd built a second brain with no self-awareness. And then I'd told a bunch of people on the internet to build one just like it.

Cool.

## The Fix

I cleared my entire day. One sitting. Everything.

Changed every exposed credential. Cleaned out the backup history twice, once to strip 13GB of video files, once to purge every leaked secret. Rebuilt the cloud backup from scratch. Merged 76 fragmented memory files into 4. Killed the zombie workers.

14GB down to 1GB. 76 files down to 4. Two dead workers removed from a schedule that had been screaming into the void for weeks.

But cleaning up the mess is just cleaning up the mess. The fix was making sure it couldn't happen again.

One rule. Every worker. No exceptions.

## The Receipt Rule

No automation gets to say "done."

**Check before you start.** Every worker confirms its job still exists and the tools it needs are actually there before it touches anything. If the check fails, it doesn't start. It doesn't report "done." It reports what's missing and stops.

**Leave a receipt.** Every worker writes a timestamped entry in a place I actually look. Not in some system folder buried six levels deep. Inside my vault, on my desk, where I see it every morning. Date, what it did, what it found. If I open my vault and the receipt isn't there, something broke.

**Fail loud.** A skipped day is logged as skipped. An error exits screaming. Silent success is treated as a lie until there's a receipt on the table.

Think of it like a security guard doing rounds. The old system: the guard says "all clear" every morning regardless of whether they actually walked the building. The new system: the guard has to scan a checkpoint in every room and the scan log is on your desk by 7am. No scan, no "all clear."

## 1,378

That night the system ran for real for the first time in weeks.

The memory worker found the right location. Read the conversation files. Consolidated weeks of accumulated work into structured notes. 1,378 messages processed. Receipt written. Timestamped. Sitting in the vault where I could see it with my own eyes.

The gut feeling had been right the entire time. The vault was stale. The system was broken. Every report said otherwise, and every report was wrong.

Trust your gut over your reports. Then fix the reports so you never have to.
