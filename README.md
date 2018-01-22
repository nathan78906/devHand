# devHand
The best helping hand for developers (ACTIONS ON GOOGLE)

## Inspiration
We were very interested in using the Google Actions for Google Assistant. We wanted to expand on the Google Home's main use which is to make life more convenient. We felt a need for Google Assistant helping developers while they code; providing them with solutions to common dev related problems.

## What it does
devHand is a Google Action for the Google Assistant. You can ask it any dev related question and it will search Stack Overflow for an appropriate answer and read it back to you. A window pops up with the full answer to help the developer out more.

## How we built it
We used Dialogflow to make an action on Google application. Then the actions on Google application was connected to a simple Python Flask server, which listened for the speech to text query from the Google Home Mini. Then the query was ran through the Stack Overflow API to search for any questions/answers. The answer (if applicable) was sent back to the Google Home Mini and read out loud, and the full answer was sent through a web socket to a client running on a PC. This displayed the answer on the developer's PC. 

## Challenges we ran into
We couldn't decide between a few different ideas but eventually chose this one. We each started working on 2 different ideas but it became apparent that this one was better than the other and more impressive. We also had trouble parsing the answer output from Stack Overflow because it contained a lot of markdown/HTML code.

Working with the Google Cloud services wasn't consistently working and combined with the inconsistent WiFi made for a frustrating experience testing.
Working with Azure also was hard and difficult to setup so we gave up on it eventually and decided to self-host.

## Accomplishments that we're proud of
We learned how to create actions on Google Assistant which is becoming a very popular tool in 2018. 
One of our team members is proud that he is able to demo at his first hackathon.

## What we learned
We learned that sleeping for more than 4 hours during a hackathon is a good idea.

## What's next for devHand
Hopefully working with Google developers to further bring our action to the market as ourselves being developers would benefit from this as well as other developers.
