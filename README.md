# msnmatch

This is a website designed for UVa(University of Virginia) Students with following features
- Student matching
- Reviews and ratings of courses and professors
- Live comments + Google slide

## Student Matching
A new version will be available this semester.

## Hoosmyprofessor
A new version will be available this semester.
- Courses and Reviews from 2016 Fall
- Admin needs to change Year and Semester manually
- Student can't be in more than one sections of a course
  - Implemented for the purpose that each user can only have one review for a course
  - Problems with courses like CS4501
  - To be fixed
- "You may also like" Function - TBD
- Recommended courses for first-years - TBD
- Automatic update of courses - TBD

## Live Comments
Designed for "IF YOU ARE THE ONE 2020", and can also be used for future activities. 
- Use of existing Comments Library
  - CommentCoreLibrary (//github.com/jabbany/CommentCoreLibrary) - Licensed under the MIT license
- Integrated with Google Slide with iframe
- Live comments and questions with WebSocket
- Manual filtering of comments and questions
- Using Heroku Redis
- Comments not scrolling smoothly - To Be Fixed