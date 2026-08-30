# ApplySei

### *By the Cloud. For the Cloud.*

ApplySei is a personal cloud job-search automation project I built to solve a problem I was experiencing myself.

## Why I Built It

There were three reasons behind ApplySei.

### 1. My previous cloud projects were expensive to keep alive

Some of my earlier cloud projects relied on infrastructure that continued to incur costs every month.

Eventually, I had to decommission them.

The problem wasn't that those projects weren't useful. They were.

But when the main point of a project is to demonstrate cloud infrastructure, keeping that infrastructure running indefinitely just for a portfolio doesn't always make financial sense.

So I wanted to build something that used cloud infrastructure **because it had a real purpose**, rather than keeping resources alive just to say I had deployed something.

### 2. The projects themselves were difficult to showcase

With my previous cloud projects, the most interesting part wasn't necessarily the application code.

It was the **infrastructure**.

There is only so much of that you can demonstrate through a GitHub repository. You can explain what each service does, but the actual project is often the way all those services work together.

I wanted to build something where the cloud infrastructure was not just supporting the project.

**The infrastructure was the project.**

And this time, I wanted something I could actually keep running and demonstrate.

### 3. My job search was painfully inefficient

While searching for Cloud, AWS, DevOps, SRE, and Infrastructure roles, I was spending a ridiculous amount of time checking career pages manually.

And I kept running into the same two problems.

I'd find a bunch of irrelevant jobs.

Or I'd find a role that looked perfect, spend 15–20 minutes going through the job description, analysing it, and deciding whether it was worth applying to...

Only to realise:

**I'd already applied to it.**

At some point, I thought:

> *Why am I manually doing this?*

So I decided to build something that could do the repetitive part for me.

Something that could find jobs, analyse them, score them based on relevance, remember what I'd already seen, and send the new ones directly to me.

That became **ApplySei**.

## What ApplySei Does

Every morning, ApplySei automatically searches for job opportunities from configured sources.

It then analyses the jobs, filters out irrelevant roles, scores the remaining opportunities based on keyword relevance, checks whether I've already seen the job, and sends new relevant opportunities directly to my Telegram.

In other words:

**I stopped searching for jobs manually and built something to search for them instead.**

**# 2. How It Works — The Technical Side**

There are two ways to understand how ApplySei works:

1. **The technical side** — how the different services and components work together.
2. **The simple side** — what actually happens when ApplySei runs, without all the technical terminology.

Let's start with the technical side.

**## Overall Architecture**

The complete architecture of ApplySei:

![ApplySei Architecture](Arch_diagram.png)

At a high level, the system follows this flow:

**EventBridge Scheduler → AWS Lambda → Python Pipeline → Firecrawl → Job Analysis & Scoring → DynamoDB + Telegram**

### Amazon EventBridge Scheduler

Amazon EventBridge Scheduler is responsible for automatically starting the pipeline.

It is configured to trigger the AWS Lambda function every day at **8:00 AM**.

This means the entire job-search process starts automatically without me having to run anything manually.

### AWS Lambda

AWS Lambda runs the main ApplySei Python application.

When EventBridge triggers the function, Lambda starts the complete pipeline — from fetching jobs to analysing, scoring, storing, and notifying.

Using Lambda also means I don't need to keep a server running 24/7 for a process that only needs to run once a day.

### Python

Python contains the core application logic behind ApplySei.

It coordinates the different stages of the pipeline and is responsible for:

* Processing the data returned by Firecrawl
* Analysing job titles and descriptions
* Applying keyword-based filtering
* Calculating relevance scores
* Structuring the job information
* Checking DynamoDB for previously processed jobs
* Sending notifications to Telegram

### Firecrawl

Firecrawl is responsible for the **job discovery and data extraction** stage.

It crawls the configured career pages and fetches the available job information and job descriptions.

Once the data is returned to the Python application, Firecrawl's job is done.

**Firecrawl collects the data. ApplySei decides what to do with it.**

---

**## Inside the Job Processing Pipeline**

The next diagram shows what happens after Firecrawl returns the job data:

![ApplySei Job Processing Pipeline](Firecrawl.png)

The retrieved job information is passed to the Python application, where the actual analysis and scoring takes place.

### Job Analysis

The application analyses the job title and job description to determine how relevant the opportunity is to the types of roles I'm looking for.

The system is primarily focused on roles around:

* Cloud
* AWS
* DevOps
* SRE
* Infrastructure
* Platform Engineering

### Keyword-Based Ranking & Scoring

ApplySei uses a **rule-based scoring system** rather than an LLM to rank jobs.

Relevant keywords contribute positively to the score, while keywords associated with unwanted domains or roles contribute negatively.

In simple terms:

**Relevant keyword → + score**

**Off-domain keyword → − score**

This allows the system to determine whether a job is worth sending to me based on explicit and understandable rules.

I intentionally chose this approach because the scoring should be:

* Predictable
* Explainable
* Cheap to operate
* Easy to modify

### Structured Job Data

Once the job has been analysed and scored, the relevant information is structured into a consistent format.

This allows the same downstream process to handle jobs regardless of where they originally came from.

The structured job data is then sent to two places.

---

**## Amazon DynamoDB**

Amazon DynamoDB acts as the persistent storage layer for ApplySei.

The database stores the jobs that have already been processed.

This gives ApplySei a memory of what it has seen before.

When the same job is fetched again during a future run, the application checks DynamoDB before sending a notification.

**Already stored → Skip it**

**New job → Store it and continue**

This prevents the same job from repeatedly appearing in my Telegram notifications.

---

**## Telegram Bot API**

Telegram is the final delivery layer.

When ApplySei finds a new and relevant job, the structured job information is sent directly to my Telegram bot.

This means that instead of opening multiple career pages every morning, I receive the relevant new opportunities directly.

---

**## The Complete Technical Flow**

Putting everything together:

**EventBridge Scheduler**

↓

**AWS Lambda**

↓

**Python Application**

↓

**Firecrawl**

↓

**Job Data + Job Description**

↓

**Job Analysis**

↓

**Keyword-Based Ranking & Scoring**

↓

**Structured Job Data**

↓

**DynamoDB Check**

↓

**New Job → Store + Send to Telegram**

**Existing Job → Skip**

The result is a serverless, automated job-discovery pipeline that runs every morning without manual intervention.
