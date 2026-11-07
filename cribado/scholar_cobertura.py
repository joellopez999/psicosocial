import csv,re,unicodedata
def key(t):
    t=unicodedata.normalize('NFD',t.lower());t=''.join(c for c in t if not unicodedata.combining(c))
    w=re.sub(r'[^a-z0-9 ]',' ',t).split()[:8];s=' '.join(w);h=5381
    for c in s:h=((h*33)^ord(c))&0xFFFFFFFF
    n='';
    while h:n='0123456789abcdefghijklmnopqrstuvwxyz'[h%36]+n;h//=36
    return n or '0'
ks="""s4i406,xrs3fk,132akbv,1t86d6u,1xa6ipj,g337f2,qdqqfn,1o0v2l5,1gqrjpb,178tkp4,1xhg03l,8o6yw,uk9gxo,6tgd1f,1euwo62,1dp5p6o,193f2qp,1drjxdj,144vuvn,11vs0at,387tor,11vbnev,1ml9k38,1cfuchg,38gskb,1ju73r,1o4huh2,1mjrt63,1ggswg6,rubwho,1h4q0wb,1gser55,by0iln,vxfp51,xlruo4,1uca2ou,1liy6cb,1nbg4nn,juh6uu,1bynu9u,2pk436,r8fivv,106dl9l,1pwmeg,1d10vk2,1u8tcy9,rlahta,86ss0s,9h6hvt,4xaya4,qxskui,1bd9oe9,10d0lpx,1nzsipj,vffgfh,12sa2o,i85bi2,lx09nv,sfgrk9,oatx1w,1y6315d,1gknu0,ui1fwj,8ahqx1,cartxl,ptp4s9,19grbk2,1dp3kzr,1u3q3iw,3h659a,bhlu6s,9v18wz,vzi710,f3ho1u,1tukoqr,uwsq5q,13gfzag,188djf,1ypdfv3,wisk8y,w6wte1,xza59o,ouc6eb,1b7wwqe,1icmv9c,1r4s3xl,1p1ynlu,1cqayhk,1q0z0vq,1hjp56w,1esmg9g,uewxkx,1m8xnpb,12i37io,v9o3o1,1ormoxe,a0ijuk,vbop6t,15i1fzo,1oi8ilk,puguce,10ai4if,2hcu8d,5hxa1f,105lml0,1dlap2b,17pn4ww,n7002b,1s3cs2o,tzhusl,11fyxa1,1j3f6yi,tdgqdh,x14nwa,5twxju,91gt98,h6r4zf,1dof0y9,jylif3,1kdypph,1ar33d,1qtpmuo,w6hiz0,1e7t37,1d4vi5o,1lyynit,5814hd,l6f03q,1e4zr6t,1j02zjx,4jskde,ellka8,bvkrhy,1rznxm8,10xj5p4,12ryde2,mtt8pf,wp7lpo,b9hgdw,13y8vld,23uqjj,1lj2dcu,1qu5i4w,yo2moj,lz6e3q,lm6mf5,12iviys,gd4rok,ko5gi4,2b1g91,17q4cdw,1ampcl9,1rtgwe4,13qou1k,ckv49e,12hvjdz,1hsm15p,whykdr,s6yhe3,yfur6d,g87dn,jc0a42,n7l9bt,1nr1t4i,1ivj0ff,r3dpv1,ibrrk9,kmpgdo,x835s8,1b4qjt2,snxr9h,1pzmay6,1q8i53u,1ob6hpk,198icfx,mutd4q,1fd4j2s,ikb0tt,xieoje,kd9fzp,4c21fk,1xtzs7o,1hmnoh7,hk23b8,8prxls,1l7vc6n,f8rasm,a2h89l,1qi69v9,1sy4i8k,i7sz42,18ary7z,m9anz7,1w8u9e9,o8zzw4,1cdb6zi,13cj5ec""".split(',')
base={}
for x in csv.DictReader(open('base/unicos.csv',encoding='utf-8-sig')): base[key(x['titulo'])]=x['fuente']
hit=[k for k in ks if k in base]
print(len(ks),'claves; en base:',len(hit),'; faltan:',len(ks)-len(hit))
