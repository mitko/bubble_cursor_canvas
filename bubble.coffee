
datalog = []

colors = 
  target: "#43E645"
  distractor: "#858585"
  base: "#E3E3E3"
  mouse: "#EB2D2D"

simplified_situation = (sit) ->
  s2 = {}
  s2.distractors = sit.distractors.length
  s2.args = sit.args
  s2.cursor_type = sit.cursor_type
  s2.mouse = sit.mouse
  s2.target = sit.target
  s2
  
situation_counter = 0
situation = situations[0]
datalog.push(["Situation",simplified_situation(situation)])
#document.Show.dataplace.value = JSON.stringify(datalog,null)

# debug data
#situation = 
#  target: [[300, 200, 100]]
#  distractors: [[600, 200, 40]]
#  mouse:
#    cursor_type: 'Bubble' #or 'point'
#    x: 0
#    y: 0  


square = (x) -> x * x
distance = (x1,y1,x2,y2) ->
  Math.sqrt( square(x1-x2) + square(y1-y2))


drawAllColored = (thecircles,col) ->
  drawCircleAt(curr[0],curr[1],curr[2],col) for curr in thecircles

drawMouse = (x,y,r,col) ->
  ctx = $('#bubble_tea')[0].getContext("2d")
  ctx.fillStyle = col
  ctx.globalAlpha = 0.5
  ctx.beginPath()
  ctx.arc(x, y, r, 0, Math.PI*2, true)
  ctx.closePath()
  ctx.fill()  
  ctx.globalAlpha = 1
  
sortfn = (ic1,ic2) ->
#  document.Show.debug3.value = ic1[0] - ic2[0]
  ic1[0] - ic2[0]
  
same_circle = (c1,c2) ->
  if c1[0]==c2[0] and c1[1]==c2[1] and c1[2]==c2[2]
    true
  else
    false  
  
  
drawSituation = (sit) ->
  #clean first
  drawCircleAt(450, 450, 1000, colors.base)

  drawAllColored(situation.target,colors.target)
  drawAllColored(situation.distractors,colors.distractor)  
 
  all_circles = situation.target.concat(situation.distractors)
  #intersect and containment distances
  icd = [[distance(situation.mouse.x,situation.mouse.y,c[0],c[1])-c[2],
    distance(situation.mouse.x,situation.mouse.y,c[0],c[1])+c[2],c] for c in all_circles][0]
     
  icd.sort(sortfn)
  
  closest = icd[0]
  second = icd[1]
  mouse_type = situation.cursor_type
  
  if mouse_type == "Bubble"
    mouse_radius = Math.min(closest[1],second[0])
  else
    mouse_radius = 0
    
  if mouse_radius == second[0]
    c = closest[2]
    drawCircleAt(c[0],c[1],c[2]+3,colors.mouse)
#  document.Show.debug.value = mouse_radius

  drawMouse(situation.mouse.x,situation.mouse.y,mouse_radius,colors.mouse)



drawCircleAt = (xpos,ypos,radius,col) ->
  ctx = $('#bubble_tea')[0].getContext("2d")
  ctx.fillStyle = col
  ctx.beginPath()
  ctx.arc(xpos, ypos, radius, 0, Math.PI*2, true)
  ctx.closePath()
  ctx.fill()
  

drawAllCircles = (thecircles) ->
  drawCircleAt(curr[0],curr[1],curr[2],curr[3]) for curr in thecircles

current_time = () ->
  d = new Date()
  [d.getHours(),d.getMinutes(),d.getSeconds(),d.getMilliseconds()]
  
getMouseXY = (e) ->
  situation.mouse.x = e.pageX-6
  situation.mouse.y = e.pageY-7
#  document.Show.MouseX.value = situation.mouse.x;
#  document.Show.MouseY.value = situation.mouse.y;  
  redraw()

processClick = (e) ->
  all_circles = situation.target.concat(situation.distractors)
  #intersect and containment distances
  icd = [[distance(situation.mouse.x,situation.mouse.y,c[0],c[1])-c[2],
    distance(situation.mouse.x,situation.mouse.y,c[0],c[1])+c[2],c] for c in all_circles][0]
     
  icd.sort(sortfn)
  closest = icd[0]
  if situation.cursor_type=='Bubble' and same_circle(closest[2],situation.target[0])
    datalog.push(["Clicked",current_time(),[e.x,e.y]])
    changeSituation(e) 
  if situation.cursor_type=='Point' and distance(situation.mouse.x, situation.mouse.y, closest[2][0], closest[2][1])<=closest[2][2]
    datalog.push(["Clicked",current_time(),[e.x,e.y]])
    changeSituation(e)   

  
changeSituation = (e) ->
  situation_counter += 1 
  situation = situations[situation_counter]
  situation.mouse.x = e.x
  situation.mouse.y = e.y
  datalog.push(["Situation",simplified_situation(situation)])
#  document.Show.dataplace.value = JSON.stringify(datalog,null)
  drawSituation(situation)
  
showData = (e) ->
  document.Show.dataplace.value = JSON.stringify(datalog,null)
  
redraw = () ->
  drawSituation(situation)
  
  
init = () ->
  document.captureEvents(Event.MOUSEMOVE)
  document.captureEvents(Event.MOUSECLICK)
  document.onmousemove = getMouseXY  
  document.onclick = processClick
  $("#generate_data").onclick = showData
  
init()
