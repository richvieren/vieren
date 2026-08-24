---
title: "My Second Brain Gaslit Me for Months"
date: 2026-07-16
description: "For weeks something felt off. My AI-powered knowledge vault, the one that automatically organized my work every night at 2am, felt frozen. Stale. Like…"
tags: []
draft: true
# imported from vieren/articles/drafts/2026-07-16-my-second-brain-gaslit-me-tucker-v3.md
originalStatus: draft-tucker-v3
flavor: tucker (structure-locked)
---

For weeks something felt off. My AI-powered knowledge vault, the one that automatically organized my work every night at 2am, felt frozen. Stale. Like walking into your apartment and knowing someone's been in there, but nothing's obviously moved.

But every report said "success." Every automated worker reported done. I'd check the status, scan the timestamps, and there it was: green lights across the board.

So I did what you do. I assumed I was imagining it.

I was not imagining it.

## The Setup Everyone Dreams About

Here's what I built. A digital vault as the knowledge base. An AI agent as the brain. Six automated workers running around the clock: one consolidating my notes every night, one backing up the vault every five minutes, one capturing messages from my phone, one pulling in research from the web. All of it humming in the background like a team of invisible assistants who never take a day off.

The dream stack. Fully automated second brain. The kind of setup people write those viral threads about.

I wrote one of those threads, too. Built the system, documented the system, told people how to build the system. With the energy of a man who had solved personal knowledge management forever.

I had not solved shit.

## Pulling the Thread

One day I finally stopped trusting the reports and looked at the actual vault.

The nightly memory worker had been clocking in on schedule, reading my AI conversations, filing them into long-term memory. Clean, reliable, disciplined. One problem: the AI tool had moved where it stores conversations. Nobody told the worker. The worker didn't care. It showed up to the old address every night, found an empty room, filed nothing, and reported "done."

Imagine hiring a night-shift employee to sort your mail, and they show up every night to an empty mailbox because the post office changed your address. And every morning they hand you a report that says "all mail sorted." For weeks. Not great.

That was the first one.

The backup system had been taking snapshots of my vault every five minutes, just like I set it up. Beautiful, disciplined snapshots. I'd assumed it was also uploading them to the cloud. It was not. The upload had been silently failing since I changed a credential and forgot this system existed. 2,451 snapshots stranded on my laptop. Backed up nowhere. Like writing a novel in a house with no fire insurance and feeling safe because you hit save a lot.

That was two.

Two more automated workers were assigned to tasks that no longer existed. I'd reorganized things during a cleanup, forgot to update their assignments. They'd been showing up to work every day, failing, writing an error into a report nobody reads, and clocking out. Every day. For weeks.

Three and four.

The vault had ballooned to 14GB. For context, a folder of text notes should be a few hundred megabytes. The five-minute snapshots had been faithfully saving everything, including massive video files I'd pulled in for research and never cleaned up. The backup system never forgets. Every video stored forever, compounding every five minutes. Fourteen gigabytes. I actually laughed.

Five.

And the one that made my stomach drop: the save-everything habit had swept private credentials into the backup history. A master database access code. Service credentials. And one, my personal favorite, sitting in plain text in the worker schedule itself. Like writing your banking PIN on the outside of your front door and feeling safe because nobody's mentioned it.

## One Design Flaw, Five Times

I sat there looking at all of it. Five different failures. Five different symptoms. One cause.

Every worker was allowed to claim "done" without proving it.

"I ran" was treated as "I worked." The memory worker didn't check whether it actually found anything to file. The backup didn't check whether the upload went through. The other workers didn't check whether their assignments still existed.

The system that's supposed to remember everything had no memory of whether it itself was working.

I'd built a second brain with no self-awareness. A knowledge base that couldn't know what it didn't know. Every piece functioned exactly as designed. The design just never asked the question: did you actually do the thing?

And then I'd told a bunch of people on the internet to build one just like it. Cool.

## One Long Day

I cleared my entire day. One sitting. Everything.

Changed every exposed credential. Cleaned out the backup history twice, once to strip 13GB of video files, once to purge every leaked secret. Rebuilt the cloud backup from scratch. Merged 76 fragmented memory files into 4. Killed the zombie workers.

14GB down to 1GB. 76 files down to 4. Two dead workers removed from a schedule that had been screaming into the void for weeks.

But cleaning up the mess is just cleaning up the mess. The real fix was rewriting every single worker under one rule.

## The Receipt Rule

No automation gets to say "done."

It has to prove it. Three requirements, no exceptions:

**Check before you start.** Every worker confirms its job still exists and the tools it needs are there before it touches anything. If the check fails, it doesn't start. It doesn't report "done." It reports what's missing and stops.

**Leave a receipt.** Every worker writes a timestamped entry in a place I actually look. Not in some system folder buried six levels deep. Inside my vault, where I see it every morning. Date, what it did, what it found. If I open my vault and the receipt isn't there, something broke. Think of it like a security guard who has to scan a checkpoint in every room. No scan, no "all clear."

**Fail loud.** A skipped day is logged as skipped. An error exits screaming. Silent success is treated as a lie until there's a receipt on the table.

## 1,378 Messages

That night the system ran for real for the first time in weeks.

The memory worker found the right location, read the conversation files, and consolidated weeks of accumulated work into structured notes. 1,378 messages processed. Receipt written. Timestamped. Sitting in the vault where I could see it with my own eyes.

The gut feeling had been right the entire time. The vault was stale. The system was broken. Every report said otherwise, and every report was wrong.

Now they don't.

Trust your gut over your reports. Then fix the reports so you never have to.
