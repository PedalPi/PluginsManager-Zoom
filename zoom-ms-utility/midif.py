class MidiIf:
    def __init__(self, midiaccess):
        self.midiaccess = midiaccess
        self.midiout = None
        self.devid = 0x58
        self.version = 3
        self.devstr = "50g"
        self.sysexhead = "f0520058"
        self.que = []
        self.scan = -1
        self.dump = 1
        self.supress = 0
        self.waitdata = None
        self.callback = None
        self.ready = 0
        self.pcnt = 0
        self.workpatch = new apatch()
        self.midiinport = None

        self.midiaccess.onstatechange = lambda ev: print("StateChange", ev)

        self.PortScan()
        self.SelectPort()
        if not self.midiout:
            AlertMsg("<br/>MIDI port is not found.<br/>Retry after connect ZOOM MS device.")

        self.timerid = setInterval(self.timer.bind(this), 80)

    def instSet(self):
        for id in effectlist:
            v = effectlist[id].ver
            if self.devid == 0x58:
                v = v&0xf
            elif self.devid == 0x5f:
                v = (v>>4)&0xf
            elif self.devid == 0x61:
                v = (v>>8)&0xf

            if v==0 or v > self.version:
                effectlist[id].install = -2

            elif self.devid != 0x58:
                effectlist[id].install = 1

    def recv(self, ev):
        if abort:
            return

        midirecv = MakeStr(ev.data)
        if self.dump == 1:
            if (ev.data[0] >= 0xf0:
                print(midirecv)

        elif if self.dump == 2:
            print(midirecv);

        if (not self.supress or self.waitdata == "c0") and ev.data[0] == 0xc0:
            if currentpatch != ev.data[1]  and  self.scan<0:
                SetPatchFocus(0)
                currentpatch = ev.data[1]
                DispPatch()
                SetPatchFocus(1)

        if midirecv.indexOf(self.sysexhead+"31") == 0:
            if ev.data[6] == 0:
                SetEffectState(currentpatch,ev.data[5],0)

            if ev.data[6] >= 2:
                v = (ev.data[7]&0x7f)+((ev.data[8]&0x7f)<<7)
                SetParamVal(currentpatch,ev.data[5],ev.data[6], v)
                if self.dump == 3:
                    print(ev.data[5], ev.data[6], v);

                DispPatch()

        elif midirecv.indexOf("f07e00060252") == 0:
            v = String.fromCharCode(ev.data[10],ev.data[11],ev.data[12],ev.data[13])
            self.version = parseFloat(v)
            self.devid = ev.data[6]

            if self.devid == 0x58:
                self.sysexhead="f0520058"
                self.devstr="50g"
                self.instSet()
                for id in effectlist):
                    ef = effectlist[id]
                    if ef.group=="AMP" and (ef.ver&0xf):
                        ef.param[7].max = gampcab[(v>=3)?1:0].max
                        ef.param[7].disp = gampcab[(v>=3)?1:0].disp

            elif self.devid == 0x5f:
                self.sysexhead = "f052005f"
                self.devstr = "60b"
                self.instSet()
                # 4 effects
                for id in effectlist:
                    ef = effectlist[id]
                    if ef.group == "AMP" and (ef.ver&0xf0):
                        ef.param[7].max = bampcab[(v>=2)?1:0].max
                        ef.param[7].disp = bampcab[(v>=2)?1:0].disp

            elif self.devid == 0x61:
                self.sysexhead = "f0520061"
                self.devstr = "70cdr"
                self.instSet()

            inst.ShowAll(false)
            document.getElementById("firmver").innerHTML = v

        elif midirecv.indexOf(self.sysexhead+"28") == 0
          var name=MakeName(ev.data);
          if(self.scan>=0){
            document.getElementById("waitmsg").innerHTML="Scanning Patches...("+self.scan+"/50)";
            patches[self.scan].ReadBin(ev.data);
            DispPatchName(self.scan);
            for(var ii=0;ii<6;++ii){
                  var id=patches[self.scan].GetEffectId(ii);
                  if(id  and  effectlist[id]){
                        effectlist[id].install=1;
                        var el=document.getElementById("e_"+id);
                        if(el) el.classList.add("install");
                  }
            }
            ++self.scan;
            if(self.scan>49){
              self.scan=-1;
              self.ready=1;
              midiif.Send([0xc0,currentpatch]);
              SetPatchFocus(1);
              DispPatch();
              document.getElementById("waitbase").style.display="none";
              ready=true;
              for(i=0;i<6;++i){
                var cell=document.getElementById("fnam"+(i+1));
                var cell2=document.getElementById("fnum"+(i+1));
                cell.oncontextmenu=function(ev){
                  currenteffect=parseInt(ev.target.id[4])-1;
                  SetCurrentEffect(currenteffect);
                  midiif.SendCurrentPatch();
                  PopupEffectMenu(ev.target);
                  ev.preventDefault();
                };
                cell.ondblclick=function(ev){
                  document.getElementById("effectpanelmsg").innerHTML="Add / Replace Effect";
                  document.getElementById("effectpanelbase").style.display="block";
                };
                cell.onclick=function(ev){
                  currenteffect=parseInt(ev.target.id[4])-1;
                  SetCurrentEffect(currenteffect);
                  ToggleEffect(currenteffect);
                  UpdateFocus();
                  DispPatchName(currentpatch);
                  ev.preventDefault();
                };
                cell2.onclick=cell2.oncontextmenu=function(ev){
                  currenteffect=parseInt(ev.target.id[4])-1;
                  PopupEffectMenu(ev.target);
                  SetCurrentEffect(currenteffect);
                  midiif.SendCurrentPatch();
                  ev.stopPropagation();
                  ev.preventDefault();
                };
              }
            }
            else{
              self.que.push([0xc0,self.scan]);
              self.que.push([0xf0,0x52,0,self.devid,0x29,0xf7]);
            }
          }
        else:
            patches[currentpatch].ReadBin(ev.data)
            for i in range(6):
                id = patches[currentpatch].GetEffectId(ii)
                if id and effectlist[id]:
                    effectlist[id].install = 1
                    el = document.getElementById("e_"+ id)
                    if el:
                         el.classList.add("install")

                DispPatch()
                DispPatchName(currentpatch)

        if self.waitdata:
            if midirecv.indexOf(self.waitdata)==0:
                self.supress = 0
                self.waitdata = null
                if self.callback:
                    self.callback(ev.data,midirecv);


    def StartScan(self):
        print("StartScan")
        if !self.midiout:
            return

        self.SendDirect([0xf0,0x7e,0x00,0x06,0x01,0xf7])

        setTimeout(function(){
          self.SendDirect([0xf0,0x52,0x00,self.devid,0x50,0xf7]);
          self.scan=0;
          setTimeout(function(){
            self.SendWait([0xf0,0x52,0x00,self.devid,0x33,0xf7],"c0",function(dat){
              self.norg=currentpatch=dat[1];
              self.que.push([0xf0,0x52,0x00,self.devid,0x50,0xf7]);
              self.que.push([0xc0,self.scan]);
              self.que.push([0xf0,0x52,0,self.devid,0x29,0xf7]);
            });
          }, 100);
        }, 200);
      };

    def SendDirect(self, d):
        if self.dump == 4:
            print("S:" + MakeStr(d))
        if self.midiout:
            self.midiout.send(d)

    def Send(self, d):
        if self.que.length > 2:
            d2 = self.que[self.que.length-1]

            if d[0]==0xf0 and d2[0]==0xf0:
                if d[4]==0x28 and d2[4]==0x28:
                    self.que.pop()
                elif d[4]==0x31 and d2[4]==0x31 and d[5]==d2[5] and d[6]==d2[6]:
                    self.que.pop()
        self.que.push(d)


    def RequestPatch(self):
        self.Send([0xf0,0x52,0x00,self.devid,0x29,0xf7])
        #self.SendWait([0xf0,0x52,0x00,self.devid,0x29,0xf7], self.sysexhead+"28", null)

    def SendParamChange(self, f, p, v):
        cmd = [0xf0,0x52,0x00,self.devid,0x31,f,p,v&0x7f,(v>>7)&0x7f,0xf7]
        self.Send(cmd)

    def SendCurrentPatch(self):
        self.Send(patches[currentpatch].MakeBin(self.devid))

    def SendCurrentPatchVerify(self, callback):
        o = []
        len = (midiif.devid==0x5f) ? 4 : 6
        for i in range(len):
            o.push(patches[currentpatch].GetEffectId(i))

        self.SendCurrentPatch()

        def callback2(dat, str):
            s = ""

            self.workpatch.ReadBin(dat)
            for j in range(len):
                if o[j] != patches[currentpatch].GetEffectId(j):
                    var
                    el = document.getElementById("e_" + o[j])
                    if el:
                        # TODO - Plugin not installed
                        el.classList.add("notinstall");
                        if effectlist[o[j]].install == 0:
                            effectlist[o[j]].install = -1
                            s += "[" + effectlist[o[j]].name + "]"

            if callback:
                callback(s.length?s: None)

        def function():
            self.SendWait([0xf0,0x52,0x00,self.devid,0x29,0xf7],self.sysexhead+"28", callback2)

        setTimeout(function, 200)

    def SendWait(self, sd, rv, cb):
        self.supress=1
        self.callback=cb
        self.waitdata=rv
        self.SendDirect(sd)

    def timer(self):
        if abort:
          return
        
        id = 0
        cookies = document.cookie.split(";")
        
        for i in range(cookies.length):
            if cookies[i].indexOf("patcheditor=")==0):
                id=parseInt(cookies[i].split("=")[1])

        if id!=0 and id != instanceid:
            AlertMsg("Another Patch Editor is launched.<br/> This instance is no more effective. <br/>Reload?", lambda: window.location.href=url);
            abort = True
            return

        if not self.midiout or self.supress:
            return

        if self.waitdata:
            return

        if self.scan >= 0:
            if self.que.length > 0:
                d = self.que.shift()
                self.SendDirect(d)

            return

        elif self.que.length > 0:
            d = self.que.shift()
            self.SendDirect(d)
        elif self.ready and dirty > 0 and ++dirty > 40:
            dirty = 0
            if autosave
                StorePatch(currentpatch)

            self.SendWait([0xf0,0x52,0x00,self.devid,0x33,0xf7],"c0")

    def PortScan(self):
        midioutputs = []

        i=0
        outputIterator = self.midiaccess.outputs.values()
        for (var o=outputIterator.next(); !o.done; o=outputIterator.next()):
            midioutputs[i] = o.value
            op = new Option(o.value.name)
            if o.value.name.startsWith("ZOOM MS Series"):
                op.selected = True
            else
                op.disabled = True
            i++;

        inputIterator = self.midiaccess.inputs.values()
        for (var ip=inputIterator.next(); !ip.done; ip=inputIterator.next()):
            if ip.value.name.startsWith("ZOOM MS Series") and self.midiinport == null: 
                self.midiinport=ip.value
                self.recvhander=self.recv.bind(this)
                self.midiinport.onmidimessage=self.recvhander

    def SelectPort(self):
        idx = document.getElementById("midiport").selectedIndex
        if idx>=0 and midioutputs.length > 0:
            self.midiout = midioutputs[idx]
            if not self.midiout.name.startsWith("ZOOM MS Series"):
                self.midiout = null
