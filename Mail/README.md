# Mail

## Overview
This project is a front-end for an email client built with Django, HTML, CSS, and JavaScript.  
It allows users to send, receive, read, archive, and reply to emails via API calls.  
The app is designed as a **single-page application (SPA)** where JavaScript dynamically controls the views.

## Objective
- Implement client-side functionality inside `inbox.js`.
- Integrate with the provided Django API to manage emails.

## Features
- **Send Mail**: Compose and send emails using the `/emails` API route.
- **Mailbox View**: Display Inbox, Sent, and Archived messages.
  - Emails show sender, subject, timestamp, and read/unread state.
- **View Email**: Click an email to see its full content (sender, recipients, subject, body, timestamp).
  - Mark emails as read when opened.
- **Archive/Unarchive**: Toggle archive status of received emails (not available for Sent).
- **Reply**: Reply to any email with:
  - Pre-filled recipient.
  - Pre-filled subject (`Re:` prefix when needed).
  - Pre-filled quoted body with timestamp and sender info.

## Technical Details
- Built on Django with a single app `mail`.
- All server-side API routes (`/emails`, `/emails/<mailbox>`, `/emails/<id>`) are provided.
- The project focuses exclusively on **front-end logic in `inbox.js`**.
- No CSRF token is required (API routes are CSRF-exempt for this project).

