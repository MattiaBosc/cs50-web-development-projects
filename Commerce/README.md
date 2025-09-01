# Commerce

## Overview
This project is an e-commerce auction site built with Django, HTML, CSS, and JavaScript.  
It allows users to post auction listings, place bids, comment on listings, and manage a personal watchlist, similar to eBay.

## Objective
- Implement a fully functional auction platform with client-side and server-side logic.
- Enable dynamic interaction with listings, bids, comments, watchlists, and categories.

## Features
- **User Authentication**: Users can register, log in, and log out.
- **Create Listing**: Users can create a new auction listing with:
  - Title and description
  - Starting bid
  - Optional image URL
  - Optional category
- **Active Listings Page**: Displays all currently active auctions:
  - Title, description, current price
  - Optional image
- **Listing Page**: Detailed page for each auction:
  - Current price and listing details
  - Add/remove from watchlist (signed-in users)
  - Place a bid (must meet minimum and current bid requirements)
  - Close auction if user is the creator
  - View and add comments
  - Display winner if auction is closed
- **Watchlist**: Displays all listings a user has added to their watchlist.
- **Categories Page**: Browse all active listings by category.
- **Admin Interface**: Manage listings, bids, and comments via Django admin.

## Technical Details
- Built on Django with a single app `auctions`.
- Models include Users, Listings, Bids, Comments, and Categories.
- Uses Django forms for validation and user input.
- Dynamic content rendering based on user authentication.
- Customizable HTML and CSS for layouts and styling.
- Use `@login_required` decorators to restrict access to authenticated users.
