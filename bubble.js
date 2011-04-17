var changeSituation, colors, current_time, datalog, distance, drawAllCircles, drawAllColored, drawCircleAt, drawMouse, drawSituation, getMouseXY, init, processClick, redraw, same_circle, showData, simplified_situation, situation, situation_counter, sortfn, square;
datalog = [];
colors = {
  target: "#43E645",
  distractor: "#858585",
  base: "#E3E3E3",
  mouse: "#EB2D2D"
};
simplified_situation = function(sit) {
  var s2;
  s2 = {};
  s2.distractors = sit.distractors.length;
  s2.args = sit.args;
  s2.cursor_type = sit.cursor_type;
  s2.mouse = sit.mouse;
  s2.target = sit.target;
  return s2;
};
situation_counter = 0;
situation = situations[0];
datalog.push(["Situation", simplified_situation(situation)]);
square = function(x) {
  return x * x;
};
distance = function(x1, y1, x2, y2) {
  return Math.sqrt(square(x1 - x2) + square(y1 - y2));
};
drawAllColored = function(thecircles, col) {
  var curr, _i, _len, _results;
  _results = [];
  for (_i = 0, _len = thecircles.length; _i < _len; _i++) {
    curr = thecircles[_i];
    _results.push(drawCircleAt(curr[0], curr[1], curr[2], col));
  }
  return _results;
};
drawMouse = function(x, y, r, col) {
  var ctx;
  ctx = $('#bubble_tea')[0].getContext("2d");
  ctx.fillStyle = col;
  ctx.globalAlpha = 0.5;
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2, true);
  ctx.closePath();
  ctx.fill();
  return ctx.globalAlpha = 1;
};
sortfn = function(ic1, ic2) {
  return ic1[0] - ic2[0];
};
same_circle = function(c1, c2) {
  if (c1[0] === c2[0] && c1[1] === c2[1] && c1[2] === c2[2]) {
    return true;
  } else {
    return false;
  }
};
drawSituation = function(sit) {
  var all_circles, c, closest, icd, mouse_radius, mouse_type, second;
  drawCircleAt(450, 450, 1000, colors.base);
  drawAllColored(situation.target, colors.target);
  drawAllColored(situation.distractors, colors.distractor);
  all_circles = situation.target.concat(situation.distractors);
  icd = [
    (function() {
      var _i, _len, _results;
      _results = [];
      for (_i = 0, _len = all_circles.length; _i < _len; _i++) {
        c = all_circles[_i];
        _results.push([distance(situation.mouse.x, situation.mouse.y, c[0], c[1]) - c[2], distance(situation.mouse.x, situation.mouse.y, c[0], c[1]) + c[2], c]);
      }
      return _results;
    })()
  ][0];
  icd.sort(sortfn);
  closest = icd[0];
  second = icd[1];
  mouse_type = situation.cursor_type;
  if (mouse_type === "Bubble") {
    mouse_radius = Math.min(closest[1], second[0]);
  } else {
    mouse_radius = 0;
  }
  if (mouse_radius === second[0]) {
    c = closest[2];
    drawCircleAt(c[0], c[1], c[2] + 3, colors.mouse);
  }
  return drawMouse(situation.mouse.x, situation.mouse.y, mouse_radius, colors.mouse);
};
drawCircleAt = function(xpos, ypos, radius, col) {
  var ctx;
  ctx = $('#bubble_tea')[0].getContext("2d");
  ctx.fillStyle = col;
  ctx.beginPath();
  ctx.arc(xpos, ypos, radius, 0, Math.PI * 2, true);
  ctx.closePath();
  return ctx.fill();
};
drawAllCircles = function(thecircles) {
  var curr, _i, _len, _results;
  _results = [];
  for (_i = 0, _len = thecircles.length; _i < _len; _i++) {
    curr = thecircles[_i];
    _results.push(drawCircleAt(curr[0], curr[1], curr[2], curr[3]));
  }
  return _results;
};
current_time = function() {
  var d;
  d = new Date();
  return [d.getHours(), d.getMinutes(), d.getSeconds(), d.getMilliseconds()];
};
getMouseXY = function(e) {
  situation.mouse.x = e.pageX - 6;
  situation.mouse.y = e.pageY - 7;
  return redraw();
};
processClick = function(e) {
  var all_circles, c, closest, icd;
  all_circles = situation.target.concat(situation.distractors);
  icd = [
    (function() {
      var _i, _len, _results;
      _results = [];
      for (_i = 0, _len = all_circles.length; _i < _len; _i++) {
        c = all_circles[_i];
        _results.push([distance(situation.mouse.x, situation.mouse.y, c[0], c[1]) - c[2], distance(situation.mouse.x, situation.mouse.y, c[0], c[1]) + c[2], c]);
      }
      return _results;
    })()
  ][0];
  icd.sort(sortfn);
  closest = icd[0];
  if (situation.cursor_type === 'Bubble' && same_circle(closest[2], situation.target[0])) {
    datalog.push(["Clicked", current_time(), [e.x, e.y]]);
    changeSituation(e);
  }
  if (situation.cursor_type === 'Point' && distance(situation.mouse.x, situation.mouse.y, closest[2][0], closest[2][1]) <= closest[2][2]) {
    datalog.push(["Clicked", current_time(), [e.x, e.y]]);
    return changeSituation(e);
  }
};
changeSituation = function(e) {
  situation_counter += 1;
  situation = situations[situation_counter];
  situation.mouse.x = e.x;
  situation.mouse.y = e.y;
  datalog.push(["Situation", simplified_situation(situation)]);
  return drawSituation(situation);
};
showData = function(e) {
  return document.Show.dataplace.value = JSON.stringify(datalog, null);
};
redraw = function() {
  return drawSituation(situation);
};
init = function() {
  document.captureEvents(Event.MOUSEMOVE);
  document.captureEvents(Event.MOUSECLICK);
  document.onmousemove = getMouseXY;
  document.onclick = processClick;
  return $("#generate_data").onclick = showData;
};
init();