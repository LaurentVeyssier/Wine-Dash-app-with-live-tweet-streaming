# Wine-Dash-app-with-live-tweet-streaming
full app using Dash and tweepy


This app is adapted from excellent tutorials from [Eric kleppen](https://github.com/bendgame) here:
- [Dashboards in Python for Beginners and Everyone Else using Dash](https://medium.com/swlh/dashboards-in-python-for-beginners-and-everyone-else-using-dash-f0a045a86644)
- [Dashboards in Python: 3 Advanced Examples for Dash Beginners and Everyone Else](https://medium.com/swlh/dashboards-in-python-3-advanced-examples-for-dash-beginners-and-everyone-else-b1daf4e2ec0a)
- [Dashboards in Python for Beginners using Dash — Live Updates and Streaming Data into a Dashboard](https://levelup.gitconnected.com/dashboards-in-python-for-beginners-using-dash-live-updates-and-streaming-data-into-a-dashboard-37660c1ba661)

The initial code can be found [here](https://github.com/bendgame/DashApp) and has been augmented based on the above papers.

# App structure

Replicate the below structure

![image](https://user-images.githubusercontent.com/68251051/128543968-7128835e-d1cb-4eac-b7f9-a39ebeba5ee2.png)

![image](https://user-images.githubusercontent.com/68251051/128544206-26afc150-16cc-4b4e-bdc8-53f715b2f75f.png)

![image](https://user-images.githubusercontent.com/68251051/128544248-40c921c3-8b13-4338-a07b-62e5d3e7209c.png)

![image](https://user-images.githubusercontent.com/68251051/128544294-3147c123-8bbd-468f-94f4-7cf29691d85b.png)

# Required modules
the following modules will be specifically required
- dash (for the dashboard)
- plotly (to visualize data within the interactive dashboard)
- tweepy (to stream live tweets)
- sqlite3 (for the kaggle wine database)

A twitter dev account is necessary and a twitter API app should be created. The credentials should be used and stored in the config.py file.

![image](https://user-images.githubusercontent.com/68251051/128545257-2eed0d16-790c-4764-b3fc-8931bfb8a919.png)


Finally the wine database can be found on the author's github winapp repository (link above).

# How to run the app
The streaming program and the dash application must be run in parallel. The streaming app should be run in one instance `python tweepystream.py` then the dash app should be run in another instance `python index.py`.
This will allow to have livefeed tweet update in the dash app.


