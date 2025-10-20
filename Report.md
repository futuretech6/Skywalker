<center><font size=7>《计算机图形学》大作业报告</font></center><br /><div align='right'><font size=4><b>陈希尧</b> 3180103012 (单人)</font><br /><div align='right'><font size=4>指导老师：吴鸿智</font></div>

[TOC]

# Intro

## Concept

通过实现基于OpenGL的模拟飞行游戏，巩固课堂所学的图形学基础知识，熟练对OpenGL功能的使用， 并掌握新的OpenGL功能的使用方式。

## Usage

### Env

`pip install -r requirements.txt`

### Config

飞船模型在game\.py:58处更改(由于每个模型要不同的配置，因此没法写进config，见谅)

天空盒在config\.py:37处更改

### Control

基础控制

* 空格开始游戏
* wsad 上下左右
* v 切换第一人称和第三人称视角
* p 暂停
* r 开启漫游(仅在暂停时按r能控制镜头移动，游戏中按r只是解除了镜头对飞船的跟随)
* esc/q 退出游戏

漫游控制

* wsad 前后左右
* lk 上下
* 双击鼠标拖移控制视角

## File Struct

```
.
├── Makefile
├── README.md
├── Skywalker.py
├── config.py
├── materials
│   ├── NCC-1701
│   ├── Starship
│   ├── ast_lowpoly2
│   ├── millenium-falcon
│   ├── sky
│   │   ├── canteen
│   │   ├── lake
│   │   └── nasa.jpg
│   └── spaceship
│       ├── propulsortext.png
│       ├── spaceship.mtl
│       ├── spaceship.obj
│       └── spaceshiptextura.png
├── modules
│   ├── camera.py
│   ├── game.py
│   ├── light.py
│   ├── methods.py
│   ├── model.py
│   ├── objLoader.py
│   ├── skybox.py
│   └── sphere.py
└── requirements.txt
```

## Requirements met

* 基于 OpenGL/WebGL，具有基本体素（立方体、球、圆柱、圆锥、多面棱柱、多面棱台）的建模表达能力；
* 具有基本三维网格导入导出功能（建议 OBJ 格式）；
* 具有基本材质、纹理的显示和编辑能力；
* 具有基本几何变换功能（旋转、平移、缩放等）；
* 基本光照明模型要求，并实现基本的光源编辑（如调整光源的位置，光强等参数）；
* 能对建模后场景进行漫游如 Zoom In/Out, Pan, Orbit, Zoom To Fit等观察功能。
* 漫游时可实时碰撞检测

## Environments

System: macOS Catalina 10.15.6

Interpreter: Python 3.6.12

Thirdy-party nodules: pygame 2.0, pyopengl 3.1, numpy 1.19



# Modules

## Game Logic

### Flowchart

```flow
st=>start: 开始
space=>condition: 按下space？
op=>operation: 一顿操作猛如虎
col=>condition: 碰撞？
deshield=>operation: 减护盾值
dead=>condition: 失去护盾？
gg=>operation: 游戏结束

st->space(no)->space(yes)->op->col(no)->op
col(yes)->deshield->dead(no)->op
dead(yes)->gg->space
```

### Ship

飞船的行为主要是移动翻转，移动就不用说了，直接修改xz轴坐标即可；翻转的逻辑如下：左右移动时沿y轴翻转，上下移动时沿x轴翻转，当没有移动时会恢复至初始的未翻转状态。飞船的状态通过函数`ship_update`来更新，以左转为例：

```python
if keys[pygame.K_a]:
    if ship.pos[0] > -x_limit:
        ship.pos[0] -= ship_speed * delta_time
    if ship.rot_y <= ship.rot_y_init - MAX_TILT_ANGLE_Y:
        ship.rot_y = ship.rot_y_init - MAX_TILT_ANGLE_Y
    else:
        ship.rot_y -= tilt_speed * delta_time
```

恢复部分以水平方向的恢复为例：

```python
if not keys[pygame.K_a] and not keys[pygame.K_d]:  # Restore
    if ship.rot_y < ship.rot_y_init - tilt_speed * delta_time:
        ship.rot_y += tilt_speed * delta_time
    elif ship.rot_y > ship.rot_y_init + tilt_speed * delta_time:
        ship.rot_y -= tilt_speed * delta_time
    else:
        ship.rot_y = ship.rot_y_init
```

### Asteroids

对于小行星带，使用一个数组将其串起。在初始化时添加`MAX_DISPLAY_AST`个小行星。

所有小行星都会以一定的速度向y轴负方向移动，营造出一个飞船在向前运动的错觉，当小行星到达y=`AST_RST_POS`处就会重新获得一个在立方体`([ship_x - AST_RANGE, ship_y + AST_RANGE], [AST_Y_MIN, AST_Y_MAX], [ship_z - AST_RANGE, ship_z + AST_RANGE])`范围内随机生成的位置，然后继续沿y^-^方向移动。这样类似于瀑布的实现能保证无论飞船如何移动周围都能有小行星。

小行星自身的旋转和移动（并非相对飞船的移动，而是其本身的移动）在[显示部分](#Render)介绍。

### Collision

由于使用的飞船和小行星模型近似于球体，因此专门实现一个类`Sphere`用以进行碰撞的检测（其实是为了测试的时候能显示出来碰撞是否正确，不然根本不需要这个类）。

对于所有的模型，半径使用模型中离中心最远的顶点到中心的距离。在游戏中，依次检测每个小行星中心到飞船中心的距离并与他们的半径之和进行比较。

## Display

### Model

#### Obj Loader

需要两部分，一部分读取obj文件本身，一部分读取mtl文件，其中：

obj文件使用的关键字

* v: 表示本行指定一个顶点，此关键字后跟着3个单精度浮点数，分别表示该顶点的X、Y、Z坐标值
* vt: 表示本行指定一个纹理坐标，此关键字后跟着2个单精度浮点数，分别表示此纹理坐标的U、V值
* vn: 表示本行指定一个法线向量，此关键字后跟着3个单精度浮点数，分别表示该法向量的X、Y、Z坐标值
* g: 表示组，后面参数为组名称，指定从此行之后到下一个以g开头的行之间的所有元素结合到一起
* f: 表示本行指定一个表面，一个表面就是一个三角形图元
* usemtl: 此关键字后参数为材质名称，指定了从此行之后到下一个以usemtl开头的行之间的所有表面所使用的材质名称，该材质可以在此obj文件所附属的mtl文件中找到具体信息
* mtllib: 此关键字后参数为文件名称，指定了obj文件所使用的材质库文件(mtl文件)的文件名称

通过逐行读取obj文件，按不同的关键字提取相应的信息。

obj文件不包含面的颜色定义信息，不过可以引用材质库，材质库信息储存在一个后缀是".mtl"的独 立文件中。mtl文件是obj文件附属的材质库文件，材质库中包含材质的漫射，环境，光泽的RGB的定义值。 mtl文件使用的关键字如下：

* newmtl: 定义新的材质组，后面参数为材质组名称
* Ka: 材质的环境光（ambient color）
* Kd: 散射光（diffuse color）
* Ks: 镜面光（specular color）
* map_Ka、map_Kd、map_Ks：材质的环境，散射和镜面贴图，对应数据为贴图文件名称

定义函数material，在函数中逐行读取mtl文件中内容，并依次存入结构体中的相应数组中。

#### Render

通过调用glCallList直接显示已存储好的模型的id对应的模型，在通过基本变换将其移动到所需的位置。

游戏中的飞船在上下左右移动时会旋转，效果可以看demo视频，这部分通过临时修改模型的rot参数就可以实现，已在上文逻辑部分说明了。

另外，由于游戏中有实现小行星的自转以及惯性移动功能，因此在render之前的时候还要注意要根据自转速度和移动速度更新小行星的自转角和位置。

```python
class Model(object):
    def rotate(self):
        self.rot_angle = (self.rot_angle + self.rot_speed) % 360

if ENABLE_AST_MOVING:
    ast.pos[0] += ast.jiggle_speed[0]
    ast.pos[1] += ast.jiggle_speed[1]
    ast.pos[2] += ast.jiggle_speed[2]
ast.rotate()
```

### Skybox

建立一个边长为200，中心位置（方向与飞船保持一致）在相机（不能是飞船，否则漫游的时候会有问题）位置上的正方体，将准备好的天空和贴图直接贴上去即可（注意由于只能用三角形生成正方形，因此各面的点的顺序要一致，本项目中我使用的\[左上，右上，右下，左下\]的贴图顺序）

### Light

参考在太阳系作业中的实现，改成python即可，由于使用平行光会导致远处的小行星基本不反光，因此本实验中使用的是单一点光源，位置在game\.py:27处可以修改（建议就放在原点附近）。

### Camera

对于相机，实现一个类Camera进行包装，类中的成员变量包括

* 表示相机本身性质的：相机的三维坐标，相机视线方向的方位角和极角
* 与操作有关的：上一次拖动时的鼠标位置，鼠标是否正在点击

#### Fixed Angle

在固定视角下，只需要每次屏幕刷新时更新xyz到飞船的正后方`CAMERA_DIST`处即可。将此过程用`update`函数封装

#### Roaming

在漫游视角下，需要考虑到相机视角的移动（以方位角和极角表示），每次屏幕刷新时，读取键盘信息，若有wsadlk的按下，则更新相机的坐标，如下：

```python
if keys[pygame.K_a]:
    self.eyex -= CAM_MOVE_STEP * sin(self.azimuthAngle * D2R)
    self.eyey += CAM_MOVE_STEP * cos(self.azimuthAngle * D2R)
if keys[pygame.K_d]:
    # 与a相反，略
if keys[pygame.K_w]:
    self.eyex += CAM_MOVE_STEP * sin(self.polarAngle * D2R) * cos(self.azimuthAngle * D2R)
    self.eyey += CAM_MOVE_STEP * sin(self.polarAngle * D2R) * sin(self.azimuthAngle * D2R)
    self.eyez += CAM_MOVE_STEP * cos(self.polarAngle * D2R)
if keys[pygame.K_s]:
    # 与w相反，略
if keys[pygame.K_l]:
    self.eyex -= cos(self.polarAngle * D2R) * cos(self.azimuthAngle * D2R)
    self.eyey -= cos(self.polarAngle * D2R) * sin(self.azimuthAngle * D2R)
    self.eyez += CAM_MOVE_STEP * sin(self.polarAngle * D2R)
if keys[pygame.K_k]:
    # 与l相反，略
```

同时读取鼠标信息，如果鼠标按下的情况下有拖移，则更新相机的视角信息，如下：

```python
mouse_pos = pygame.mouse.get_pos()

for e in even_list:
    if e.type == pygame.MOUSEBUTTONDOWN:
        self.clicked = True
        self.mouse_oldx, self.mouse_oldy = mouse_pos[0], mouse_pos[1]
    if e.type == pygame.MOUSEBUTTONUP:
        self.clicked = False
print(self.clicked)
if self.clicked:
    self.azimuthAngle += (mouse_pos[0] - self.mouse_oldx) / 5
    self.polarAngle -= (mouse_pos[1] - self.mouse_oldy) / 5
    self.mouse_oldx, self.mouse_oldy = mouse_pos[0], mouse_pos[1]
```

#### Jitter

相机的抖动通过随机微调相机xz坐标位置实现，在上面两种情况下，通过传入的`isCollision`参数加入对`eyex`和`eyez`的修改：

```python
if isCollision:
    self.eyex += uniform(-CAM_SHAKE_RANGE, CAM_SHAKE_RANGE)
    self.eyey += uniform(-CAM_SHAKE_RANGE, CAM_SHAKE_RANGE)
```



# Demo

本报告主要是对技术细节实现的描述，具体的效果展示请参看附带的展示视频。



# Appendix

## Reference

https://www.pygame.org/wiki/OBJFileLoader

[What fonts can I use with pygame.font.Font? - Stack Overflow](https://stackoverflow.com/questions/38001898/what-fonts-can-i-use-with-pygame-font-font)

