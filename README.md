# slack-karma
Add the karma bot to slack just as it work in Hipchat
It use AWS S3 to store the points.
### How to setup:

Create a new Slack application, and install it to your slack space. On the app seting choose to add a bot. You will need to enter in line 7 the bot token returned by slack

If you run the script on ec2, just add a role to allow access to the bucket of your choice (and add the bucket name line 16) or you can specify aws access token line 11 and 12

The script need to run all the time

You can use http://supervisord.org/configuration.html#program-x-section-example to run the script
You need to add the bot user to every room

### How to use:

@user++ or @user-- (You can add up to 5 + or -)

thing++ or thing-- (You can add up to 5 + or -)

!karma to see your karma

!karma top to see the classment 
