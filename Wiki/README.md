# Wiki

## Overview
This project implements a Wikipedia-like online encyclopedia using **Django**.  
Each entry is stored in **Markdown format**, which is then converted to HTML for display in the browser.  
The application allows browsing, searching, creating, editing, and viewing random encyclopedia entries.

## Objective
- **Entry Page**  
  - Visiting `/wiki/TITLE` shows the contents of the corresponding entry.  
  - If the entry does not exist, display an error page.  
- **Index Page**  
  - The homepage lists all entries, each linked to its individual page.  
- **Search**  
  - If the query matches an entry title, redirect directly to that page.  
  - Otherwise, show a results page with all entries containing the query as a substring.  
- **New Page**  
  - Users can create new entries by specifying a title and Markdown content.  
  - Prevent overwriting if the title already exists.  
- **Edit Page**  
  - Entries can be edited in a textarea pre-filled with the current Markdown.  
  - Upon saving, redirect back to the updated entry page.  
- **Random Page**  
  - A link in the sidebar loads a random encyclopedia entry.  
- **Markdown to HTML Conversion**  
  - Convert Markdown content into HTML before rendering (e.g., with `markdown2`).  

## How to Use
1. Run the Django development server with `python manage.py runserver`.  
2. Open the app in a browser and navigate to the homepage to view all entries.  
3. Use the sidebar to:  
   - Search for entries.  
   - Create a new entry.  
   - Open a random entry.  
4. Click on any entry title to view its content.  
5. On an entry page, use the **Edit** option to update its Markdown content.  
