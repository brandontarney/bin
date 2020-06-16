#!/usr/bin/python
#NOTE: this require python2, python3 updates are simple but required

import os;

def log(S):
	print "__LOG '%s'"%(S);
pass;

class Diagram: 
	def __init__(self):
		self.outFile_="./out.jpg";
		self.width_=0;
		self.height_=0;
		self.msgList_=[];

	def add(self, msg):
		self.msgList_.append(msg);
	
	def textDim(self, text):
		cmd="convert label:'%s' %s"%(text,'temp.jpg');
		os.system(cmd);
		cmd="identify temp.jpg | cut -f 3 -d ' '";
		retVal=os.popen(cmd).read();
		os.system("rm temp.jpg");
		return retVal.rstrip('\n');
	
	def draw(self):
		betweenObj=100;
		objY=20;

		#--position object, heads of lifelines
		iW=betweenObj;
		for msg in self.msgList_:
			msg.src_.y_=objY;
			msg.sink_.y_=objY;
			if msg.src_.x_==0:
				msg.src_.x_=iW;
				iW+=betweenObj;
			if msg.sink_.x_==0:
				msg.sink_.x_=iW;
				iW+=betweenObj;

		#--draw message lines
		cmd="convert ";
		y=50;
		rightArrow="l -15,-5  +5,+5  -5,+5  +15,-5 z"
		leftArrow="l +15,+5  -5,-5  +5,-5  -15,+5 z"
		for msg in self.msgList_:
			src=msg.src_;
			sink=msg.sink_;
			if src.x_ == sink.x_:
				W=30;
				H=20;
				cmd+="-draw 'line %d, %d %d,%d' "%(src.x_,y, src.x_+W,y);
				cmd+="-draw 'line %d, %d %d,%d' "%(src.x_+W,y,src.x_+W,y+H);
				cmd+="-draw 'line %d, %d %d,%d' "%(src.x_+W,y+H,src.x_,y+H);
				cmd+="-draw \"path \'M %d,%d %s'\" "%(src.x_,y+H,leftArrow);
				D=self.textDim(msg.label_);
				tH=int(D.split('x')[0])/2;
				tW=int(D.split('x')[1])/2;
				cmd+="-draw 'text %d,%d \"%s\"' "%(src.x_+W+5,y+((tH)/2), msg.label_);
				y=y+H;
			else:
				cmd+= "-draw 'line %d,%d %d,%d' "%(src.x_,y,sink.x_,y);
				cmd+="-draw \"path \'M %d,%d %s'\" "%(sink.x_,y,(leftArrow if src.x_ > sink.x_ else rightArrow));
				D=self.textDim(msg.label_);
				textWidth=int(D.split('x')[0])/2;
				textHeight=int(D.split('x')[1])/2;
				cmd+="-draw 'text %d,%d \"%s\"' "%((src.x_+sink.x_)/2-textWidth, y-(textHeight/2), msg.label_);
			y+=20;
		self.height_=y+50;
		self.width_=iW;
		cmd+="-size %dx%d xc:white -fill none -stroke black "%(self.width_,self.height_);

		#--draw lifeline
		L=[];
		for msg in self.msgList_:
			src=msg.src_;
			sink=msg.sink_;
			D=self.textDim(src.name_);
			w=int(D.split('x')[0])/2;
			for obj in [src, sink]:
				draw=not (obj in L);
				if (draw):
					cmd+="-draw 'text %d,%d \"%s\"' "%(obj.x_-w,obj.y_-5,obj.name_);
					cmd+="-draw 'stroke-dasharray 5 5 line %d, %d %d,%d' "%(obj.x_,obj.y_, obj.x_,self.height_-20);
					L.append(obj);

			cmd+="%s"%(self.outFile_);
			log(cmd);
			os.system(cmd);

class Object:
	def __init__(self,name):
		self.name_=name;
		self.x_=0;
		self.y_=0;

class Message:
	def __init__(self, srcObj, sinkObj,label):
		self.src_=srcObj;
		self.sink_=sinkObj;
		self.label_=label;


# TEST PROGRAMS
def test00():
	diagram=Diagram();
	obj1=Object('object1');
	obj2=Object('object2');
	obj3=Object('object3');
	
	m1=Message(obj1,obj2,'method1(arg1)');
	diagram.add(m1);
	
	m2=Message(obj2,obj1,'return val');
	diagram.add(m2);

	m3=Message(obj1,obj1,'method2(abc)');
	diagram.add(m3);

	m4=Message(obj1,obj3,'method3()');
	diagram.add(m4);

	diagram.draw();

def test01():
	diagram=Diagram();
	diagram.draw();

def test02():
	L=[];
	for i in range(0,10):
		L.append(Object('object%d'%i));

	diagram=Diagram();
	for obj in L:
		m=Message(L[0],obj,'message x');
		diagram.add(m);
		m=Message(L[0],obj,'methodX()');
		diagram.add(m);
		diagram.add(Message(obj,obj,'ping'));

	diagram.draw();


#---main---
test00();
#test01();
#test02();

