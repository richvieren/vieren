---
title: "My Second Brain Gaslit Me for Months"
date: 2026-07-16
description: "For weeks something felt off. My Obsidian vault, the one auto-maintained by AI, consolidating my work every night at 2am, felt frozen. Stale. Like a room…"
tags: []
draft: true
# imported from vieren/articles/drafts/2026-07-16-my-second-brain-gaslit-me.md
originalStatus: draft
---

For weeks something felt off. My Obsidian vault, the one auto-maintained by AI, consolidating my work every night at 2am, felt frozen. Stale. Like a room where someone moved the furniture one inch to the left and swore they didn't touch anything.

But every log said "success." Every job reported done. I'd check the cron output, scan the timestamps, and there it was: green lights across the board.

So I did what you do. I assumed I was imagining it.

## The Setup Everyone Dreams About

Here's what I built. An Obsidian vault as the knowledge base. Claude Code as the agent. Cron jobs doing nightly memory consolidation. Git auto-syncing every five minutes. Telegram inbox capture piping messages straight into the vault. Daily scraping pulling in references and research.

The dream stack. Fully automated second brain. The kind of setup people write those viral threads about.

I wrote one of those threads, too. Built the system, documented the system, told people how to build the system.

The system was broken for months.

## Pulling the Thread

One day I finally looked. Not at the logs. At the actual vault.

The nightly memory script had been running on schedule, reading session logs from Claude Code, consolidating them into long-term memory files. Clean, reliable, disciplined. One problem: Claude Code changed its log folder structure at some point. The script kept looking in the old location. Found nothing. Consolidated nothing. And every night it printed "done" and exited successfully.

Months of sessions. Gone. Not lost, exactly. They happened. Claude Code still had them somewhere in the new location. But the consolidation layer, the part that was supposed to compound my knowledge over time, had been staring at an empty room and reporting that the room was clean.

That was the first one.

The git auto-sync had been committing every five minutes, just like I set it up. Every five minutes, a snapshot of the vault. Thousands of commits. I'd assumed it was also pushing to the remote. It was not. The push had been silently hanging on dead credentials. 2,451 commits stranded locally. Three months of version history that existed on exactly one machine.

That was two.

Two more scheduled jobs pointed at scripts that no longer existed. I'd moved them during a cleanup, forgot to update the cron entries. They'd been erroring daily into log files that nobody reads. Daily. For months.

Three and four.

The repo had ballooned to 14GB. The five-minute snapshots had been faithfully committing everything, including giant scraped videos I'd pulled in for research and never cleaned up. Git never forgets. Every binary, every frame, every 200MB video file, versioned and stored forever in the git history.

Five.

And the one that made my stomach drop: the commit-everything habit had swept live API keys into git history. A database admin key. A couple of service tokens. And one sitting in plaintext in the crontab itself, visible to anything that could read the cron table.

## One Design Flaw, Five Times

I sat there looking at all of it. Five different failures. Five different symptoms. One cause.

Every job was allowed to claim success without proving it.

Exit code 0 was treated as truth. "Script ran" was treated as "script worked." The system had no way to verify that what was supposed to happen actually happened. The memory script didn't check whether it found any logs. The git sync didn't check whether the push succeeded. The cron jobs didn't check whether their scripts existed.

The system that's supposed to remember everything had no memory of whether it itself was working.

I'd built a second brain with no self-awareness. A knowledge base that couldn't know what it didn't know. Every piece functioned exactly as designed. The design just never asked the question: did you actually do the thing?

## One Long Day

I fixed it all in a single sitting.

Rotated every exposed key. Rewrote git history twice: once to strip 13GB of binaries, once to purge all secrets. Deleted the remote and re-pushed a clean repo. Merged 76 fragmented AI-memory files into 4 consolidated ones. Killed the zombie jobs.

14GB down to 1GB. 76 files down to 4. Two dead scripts buried. Every credential rotated.

But the cleanup wasn't the real fix. The real fix was rewriting every single job under one rule.

## The Receipt Rule

No automation gets to say "done."

It has to prove it. Three requirements, no exceptions:

**Verify before acting.** Every job checks its preconditions before it touches anything. The memory script confirms the log directory exists and contains files from the last 24 hours. The git sync confirms the remote is reachable and credentials are valid. If the precondition fails, the job doesn't run. It doesn't print "done." It prints exactly what's missing and exits with a non-zero code.

**Leave a receipt.** Every job writes a timestamped entry to a status note inside the vault itself. Not to a log file in /var/log that I'll never open. Inside the vault, where I actually look. Date, what ran, what it found, what it did. If I open my vault in the morning and the receipt isn't there, something broke.

**Fail loud.** A skipped day is logged as skipped. An error exits screaming. Silent success is treated as a lie until there's a receipt on the table.

## 1,378 Messages

That night the pipeline ran for real for the first time in months.

The memory script found the new log directory, read the session files, and consolidated three months of accumulated context into structured memory notes. 1,378 messages processed. Receipt written. Timestamped. Sitting in the vault where I could see it.

The gut feeling had been right all along. The vault was stale. The system was broken. The logs just had no way to tell me.

Now they do.

Trust your gut over your logs. Then fix the logs so you never have to.
