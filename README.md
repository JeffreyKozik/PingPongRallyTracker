# PingPongRallyTracker
<ul>
  <li> Each frame, tracks movement and hones in on regions where movement has occured. https://www.youtube.com/watch?v=MkcUgPhOlP8</li>
  <li> Next, finds the contours in the regions where movement has occurred and compares the dimensions of the contour with expected dimensions of ping pong ball. Then, template matches with template of ping pong ball (simply a screenshot from the video). https://www.youtube.com/watch?v=sghglbXyjHc </li>
  <li> Determines coordinates of ping pong ball in video and deduces which side of the net the ball is on. Keeps track of when the side changes to determine rally length. </li>
  <li> Also used imutils to resize frames. https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/ </li>
</ul>
