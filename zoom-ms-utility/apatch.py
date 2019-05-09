
class apatch:
    def __init__(self):
        self.name = ""
        self.fx = [
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
        ]
        self.maxfx = 1
        self.curfx = 0
        self.dspstate = 0

    def CopyFrom(self, a):
        self.name=a.name.slice(0)
        for i in range(6):
            for j in range(11):
                self.fx[i][j] = a.fx[i][j]
        self.maxfx = a.maxfx
        self.curfx = a.curfx
        self.dspstate = 0

    empty146 = [
          0xf0,0x52,0x00,0x58,0x28,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
          0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
          0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
          0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
          0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
          0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
          0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x40,0x05,0x0f,0x45,0x00,0x6d,0x70,0x74,0x79,0x20,0x20,
          0x20,0x00,0x20,0x20,0x00,0xf7
    ]
    empty105 = [
        0xf0,0x52,0x00,0x5f,0x28,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
        0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
        0x00,0x00,0x00,0x00,0x00,0x10,0x00,0x00,0x40,0x04,0x0f,0x45,0x6d,0x00,0x70,0x74,0x79,0x20,0x20,0x20,
        0x20,0x00,0x20,0x00,0xf7
    ]
    bits = [
        [
        # eff0
            [[6,1,0]],  # State
            [[5,0x40,24],[6,0x7e,16],[7,0x07,8],[9,0x1f,0]], # ID
            [[9,0x60,-5],[5,0x8,-1],[10,0x7f,3],[5,0x4,8],[11,0x1,11]],  # Params2-
            [[11,0x7c,-2],[5,0x2,4],[12,0x1f,6]],
            [[5,0x1,0],[14,0x7f,1],[13,0x40,2],[15,0x3,9]],
            [[15,0x70,-4],[13,0x20,-2],[16,0x0f,4]],
            [[16,0x70,-4],[13,0x10,-1],[17,0x0f,4]],
            [[17,0x70,-4],[13,0x08,0],[18,0x0f,4]],
            [[18,0x70,-4],[13,0x04,1],[19,0x0f,4]],
            [[19,0x70,-4],[13,0x02,2],[20,0x1f,4],[23,0x40,"NZ"]],
            [[24,0x7f,0],[21,0x10,3]],
        ], [ 
        # eff1
            [[26,1,0]], # State
            [[21,0x4,28],[26,0x7e,16],[27,0x07,8],[30,0x1f,0]], # ID
            [[30,0x60,-5],[29,0x40,-4],[31,0x7f,3],[29,0x20,5],[32,0x1,11]],
            [[32,0x7c,-2],[29,0x10,1],[33,0x1f,6]],
            [[29,0x8,-3],[34,0x7f,1],[29,0x4,6],[35,0x3,9]],
            [[35,0x70,-4],[29,0x2,2],[36,0x0f,4]],
            [[36,0x70,-4],[29,0x1,3],[38,0x0f,4]],
            [[38,0x70,-4],[37,0x40,-3],[39,0x0f,4]],
            [[39,0x70,-4],[37,0x20,-2],[40,0x0f,4]],
            [[40,0x70,-4],[37,0x10,-1],[41,0x1f,4],[43,0x40,"NZ"]],
            [[44,0x7f,0],[37,0x1,7]],
        ], [
        # eff2
            [[47,1,0]], # State
            [[45,0x20,25],[47,0x7e,16],[48,0x07,8],[50,0x1f,0]],  # ID
            [[50,0x60,-5],[45,0x4,0],[51,0x7f,3],[45,0x2,9],[52,0x1,11]],
            [[52,0x7c,-2],[45,0x1,5],[54,0x1f,6]],
            [[53,0x40,-6],[55,0x7f,1],[53,0x20,3],[56,0x3,9]],
            [[56,0x70,-4],[53,0x10,-1],[57,0x0f,4]],
            [[57,0x70,-4],[53,0x8,0],[58,0x0f,4]],
            [[58,0x70,-4],[53,0x4,1],[59,0x0f,4]],
            [[59,0x70,-4],[53,0x2,2],[60,0x0f,4]],
            [[60,0x70,-4],[53,0x1,3],[62,0x1f,4],[64,0x40,"NZ"]],
            [[65,0x7f,0],[61,0x8,4]],
        ], [
        # eff3
            [[67,1,0]], # State
            [[61,0x2,29],[67,0x7e,16],[68,0x07,8],[71,0x1f,0]], # ID
            [[71,0x60,-5],[69,0x20,-3],[72,0x7f,3],[69,0x10,6],[73,0x1,11]],
            [[73,0x7c,-2],[69,0x8,2],[74,0x1f,6]],
            [[69,0x4,-2],[75,0x7f,1],[69,0x2,7],[76,0x3,9]],
            [[76,0x70,-4],[69,0x1,3],[78,0x0f,4]],
            [[78,0x70,-4],[77,0x40,-3],[79,0x0f,4]],
            [[79,0x70,-4],[77,0x20,-2],[80,0x0f,4]],
            [[80,0x70,-4],[77,0x10,-1],[81,0x0f,4]],
            [[81,0x70,-4],[77,0x8,0],[82,0x1f,4],[84,0x40,"NZ"]],
            [[86,0x7f,0],[85,0x40,1]],
        ], [
        # eff4
            [[88,1,0]], # State
            [[85,0x10,26],[88,0x7e,16],[89,0x07,8],[91,0x1f,0]],  # ID
            [[91,0x60,-5],[85,0x2,1],[92,0x7f,3],[85,0x1,10],[94,0x1,11]],
            [[94,0x7c,-2],[93,0x40,-1],[95,0x1f,6]],
            [[93,0x20,-5],[96,0x7f,1],[93,0x10,4],[97,0x3,9]],
            [[97,0x70,-4],[93,0x8,0],[98,0x0f,4]],
            [[98,0x70,-4],[93,0x4,1],[99,0x0f,4]],
            [[99,0x70,-4],[93,0x2,2],[100,0x0f,4]],
            [[100,0x70,-4],[93,0x1,3],[102,0x0f,4]],
            [[102,0x70,-4],[101,0x40,-3],[103,0x1f,4],[105,0x40,"NZ"]],
            [[106,0x7f,0],[106,0x4,5]],
        ], [
        # eff5
            [[108,1,0]],  # State
            [[101,0x1,30],[108,0x7e,16],[110,0x07,8],[112,0x1f,0]], # ID
            [[112,0x60,-5],[109,0x10,-2],[113,0x7f,3],[109,0x8,7],[114,0x1,11]],
            [[114,0x7c,-2],[109,0x4,3],[115,0x1f,6]],
            [[109,0x2,-1],[116,0x7f,1],[109,0x1,8],[118,0x3,9]],
            [[118,0x70,-4],[117,0x40,-3],[119,0x0f,4]],
            [[119,0x70,-4],[117,0x20,-2],[120,0x0f,4]],
            [[120,0x70,-4],[117,0x10,-1],[121,0x0f,4]],
            [[121,0x70,-4],[117,0x8,0],[122,0x0f,4]],
            [[122,0x70,-4],[117,0x4,1],[123,0x1f,4],[126,0x40,"NZ"]],
            [[127,0x7f,0],[125,0x20,2]],
          ]
        ]

    namidx = [
        [91,92,94,95,96,97,98,99,100,102],
        [132,134,135,136,137,138,139,140,142,143]
    ]

    cabbyte = [23,43,64,84,105,126,]
    v2byte = [8,28,49,70,]
    maxfxidx = [89,130,]
    
    def GetParamVal(self, effect, param):
        return self.fx[effect][param]

    def GetEffectId(self, effect):
        return self.fx[effect][1]

    def GetEffectState(self, effect):
        return self.fx[effect][0]

    def GetDspState(self, n):
        # TODO O que será isso?
        return (self.dspstate>>n) & 1

    def GetCurFxBit(self, dat):
        if dat.length<146:
            return 3-(((dat[88]&0x40)>>6)+((dat[85]&0x10)>>3))
        else:
            return 6-(((dat[130]&1)<<2)+((dat[125]&8)>>2)+((dat[129]&0x40)>>6))

    def SetCurFxBit(self, dat, n):
      if dat.length < 146:
        n =3-n
        dat[88] = (dat[88]&~0x40)+((n&1)<<6)
        dat[85] = (dat[85]&~0x10)+((n&2)<<3)

      else:
        n=5-n
        dat[129]=(dat[129]&~0x40)+((n&1)<<6)
        dat[125]=(dat[125]&~0x8)+((n&2)<<2)
        dat[130]=(dat[130]&~1)+((n&4)>>2)

    def SetMaxFxBit(self, dat,n):
        len = dat.length
        o = self.maxfxidx[len>=146?1:0]
        if n==0:
            n=1
        if n>6:
            n=6
        if len<146 and n>4:
            n=4

        dat[o]=(dat[o]&~0x1c)+(n<<2)

    def GetMaxFxBit(self, dat):
        return (dat[self.maxfxidx[dat.length>=146?1:0]]&0x1c)>>2

    def SetBits(dat,bits,val):
        len = dat.length
        blen = bits.length
        for i in range(blen):
            b0=bits[i]
            bb, v = None, None
            if b0[0] < len:
              if b0[2] == "NZ":
                dat[b0[0]]=(dat[b0[0]]&~b0[1])+(val!=0?b0[1]:0)
              else:
                if b0[2]>=0:
                  v=val>>b0[2]
                else:
                  v=val<<-b0[2]
                dat[b0[0]]=(dat[b0[0]]&~b0[1])+(v&b0[1])

    def GetBits(self, dat, bits):
        len = dat.length
        val = 0
        for i in range(bits.length):
            b0 = bits[i]
            if b0[0]<len and b0[2] != "NZ":
                r = b0[0]
                if r<len:
                    v = dat[b0[0]]&b0[1]
                    if(b0[2]>=0):
                        v<<=b0[2]
                    else:
                        v>>=-b0[2]
                    val |= v

        return val

    def ReadBin(self, dat):
        len = dat.length
        name = ""
        for j in range(13):
            c = dat[((len>=146)?132:91)+j]
            if c:
              name += String.fromCharCode(c)

        self.name = name.replace(/ +$/,"")
        flen = (len>=146)?6:4
        for f in range(f):
            for p in range(11):
                if f >= flen:
                    self.fx[f][p]=0
                else:
                    self.fx[f][p]=self.GetBits(dat,self.bits[f][p])

        self.maxfx=self.GetMaxFxBit(dat)
        self.curfx=self.GetCurFxBit(dat)
        self.dspstate = dat[(len>=146)?129:88]&0x3f

    def MakeBin(self, id):
        i, r, flen = None, None, None
        if id==0x5f:
            r = self.empty105.slice(0)
            flen = 4
        else:
            r = self.empty146.slice(0)
            flen = 6

        r[3] = id
        len = r.length
        name = self.name
        if name.length > 10:
            name=name.substr(0,10)
        for i in range(10):
            c = name.charCodeAt(i)
            r[self.namidx[(id==0x5f)?0:1][i]]=(isNaN(c)?0x20:c)

        for f in range(flen):
            for p in range(11):
                self.SetBits(r,self.bits[f][p], self.fx[f][p])

            ef = effectlist[self.fx[f][1]]
            if ef and ef.group== "AMP":
                if (ef.ver & 0xf0)==0x20:
                    r[self.v2byte[f]]=0x20
                if ef.ver&0xf:
                    r[self.cabbyte[f]]=(self.fx[f][9]?0x40:0)

                else:
                    if self.fx[f][9] == 0:
                        r[self.cabbyte[f]]=0
                    elif self.fx[f][9] in [16, 32, 48, 96, 112, 192]
                        r[self.cabbyte[f]]=0x50
                    else:
                        r[self.cabbyte[f]]=0x51

        i = (len>=146?5:3)
        while i>0:
            if self.fx[i][1]!=0:
                break
            i -= 1

        self.SetMaxFxBit(r,i+1)
        self.SetCurFxBit(r,self.curfx)
        return r

