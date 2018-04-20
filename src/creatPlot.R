
library(dplyr)
library(ggplot2)
fire=NULL
soyb=NULL
cont=NULL
if(file.exists('camfire.csv')){
  fire=read.csv('camfire.csv')  
  fire$Torre='Fire'
}
if(file.exists('tangsoy.csv')){
  soyb=read.csv('tangsoy.csv')
  soyb$Torre='Soyb'
}
if(file.exists('camcont.csv')){
  cont=read.csv('camcont.csv')  
  cont$Torre='Cont'
}

torres=plyr::rbind.fill(fire,soyb,cont)
torres$data=as.Date(torres$data)
torres$Ano=format(as.Date(torres$data,"%Y-%m-%d"),'%Y')
torres$Mes=format(as.Date(torres$data,"%Y-%m-%d"),'%m')
torres$Dia=format(as.Date(torres$data,"%Y-%m-%d"),'%d')
torres$cont=1
torres$hora=as.numeric(as.character(substr(torres$time,1,2)))

lif=doBy::summaryBy(cont~data+hora+Torre,torres,keep.names=T,FUN=sum)
lif2=subset(lif,data>Sys.Date()-90)

f1=ggplot() +   
  geom_tile(data=lif2, aes(x=hora, y=data,
            fill=as.factor(cont)), colour="white", size=0.1)+
  facet_grid(~Torre)+
  theme_bw()+
  labs(list(x = "Hour", y = "Data"),size=5)+
  theme(legend.title=element_blank(),
        axis.title.x=element_text(size=16,vjust=0.4),
        strip.text.y = element_text(angle = 90))+
  scale_fill_manual(values = c(
    '1'='#CAFF70','2'='#00FF00','3'='#5b3a05','4'='#0f0000',
    '5'='#1f0000','6'='#2f0000','7'='#3f0000','8'='#4f0000',
    '9'='#5f0000','10'='#6f0000','11'='#7f0000','12'='#8f0000',
    '13'='#9f0000','14'='#af0000','15'='#bf0000','16'='#cf0000',
    '17'='#df0000','18'='#ef0000','19'='#ff0000'))

writeChar(paste('<p></p>'),'erroSys.html',eos=NULL)
writeChar(paste('{"body":"body.html", "error":false}'),
          'openFileHTML.json',eos=NULL)
writeChar(paste(Sys.time(),Sys.timezone()),'reportTime',eos=NULL) 


ggsave(filename = "gf1.jpg", plot = f1,
       width = 29, height = 16, units =  "cm", dpi = 300)

