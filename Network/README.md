# Network

## Overview
This project is a social network web application built with Django, HTML, CSS, and JavaScript.  
It allows users to create posts, follow other users, like/unlike posts, and view feeds of posts.

## Objective
- Implement client-side and server-side logic for a Threads-like social network.
- Enable dynamic interaction with posts, profiles, and user relationships.

## Features
- **New Post**: Signed-in users can submit new text-based posts.
- **All Posts**: Display all posts from all users in reverse chronological order, showing:
  - Username of poster
  - Post content
  - Timestamp
  - Number of likes
- **Profile Page**: Clicking a username opens that user's profile page:
  - Display follower/following counts
  - Display all posts by that user (reverse chronological)
  - Show “Follow”/“Unfollow” button for other users
- **Following Feed**: Displays posts only from users the current user follows.
  - Requires user to be signed in
- **Pagination**: Posts displayed 10 per page, with Next/Previous buttons as needed
- **Edit Post**: Users can edit their own posts in place via a textarea
  - Edits update asynchronously via JavaScript
  - Users cannot edit others’ posts
- **Like/Unlike**: Users can toggle likes on any post
  - Like counts update asynchronously without reloading the page

## Technical Details
- Built on Django with a single app `network`.
- Models include Users, Posts, Followers, and Likes.
- Uses JavaScript fetch calls for asynchronous updates (edit posts, like/unlike).
- Pagination can be implemented with Django’s Paginator class and optionally styled using Bootstrap.

