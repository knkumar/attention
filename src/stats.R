library("ggplot2")

files <- list.files("results/gabor", pattern="*.csv$")

getDist <- function(trial_data) {
  twoDist <- trial_data$NumDist==2
  oneDist <- trial_data$NumDist==1
  noDist <- trial_data$NumDist==0
  return ( list(oneDist=oneDist,twoDist=twoDist,noDist=noDist) )
}

gendfRT <- function(trial_data,dists) {
  dfRT <- data.frame(Trial= trial_data[dists$noDist,]$TrialNum, RT=trial_data[dists$noDist,]$RT, Type="no distractor")
  dfRT <- rbind(dfRT, data.frame(Trial=trial_data[dists$oneDist,]$TrialNum, RT=trial_data[dists$oneDist,]$RT,Type="one distractor") )
  dfRT <- rbind(dfRT, data.frame(Trial=trial_data[dists$twoDist,]$TrialNum, RT=trial_data[dists$twoDist,]$RT, Type="two Distractor") )
  return(dfRT)
}

filter <- function(trial_data) {
  trial_data <- trial_data[trial_data$TrialNum >20,]
  tmp <- trial_data[trial_data$RT < 1500 & trial_data$RT > 300 & trial_data$NumDist == 0,]
  tmp <- rbind(tmp, trial_data[trial_data$RT < 2000 & trial_data$RT > 500 & trial_data$NumDist > 0,])
  return (tmp)
}

writeData <- function(fullData, trial_data) {
  if(length(fullData) == 0){
    fullData <- trial_data
  }
  else{
    fullData <- rbind(fullData,trial_data)
  }
  return(fullData)
}

calcAcc <- function(trial_data, dists) {
  DC <- trial_data$Response == "correct"
  DI <- trial_data$Response == "Incorrect"
  oneDist <- trial_data[dists$oneDist,]
  noDC <- trial_data[ (dists$noDist & DC), ]
  oneDC <- trial_data[ (dists$oneDist & DC), ]
  twoDC <- trial_data[ (dists$twoDist & DC), ]
  #Incorrect responses
  noDI <- trial_data[ (dists$noDist & DI), ]
  oneDI <- trial_data[ (dists$oneDist & DI), ]
  twoDI <- trial_data[ (dists$twoDist & DI), ]
  #accuracy
  noDistAcc <- nrow(trial_data[DC,])/ (nrow(trial_data[DC,])+nrow(noDI)) * 100
  oneDistAcc <- nrow(oneDC)/ (nrow(oneDC)+nrow(oneDI)) * 100
  twoDistAcc <- nrow(twoDC)/ (nrow(twoDC)+nrow(twoDI)) * 100
  return(data.frame(noDistAcc,oneDistAcc,twoDistAcc))
}

pilotStats <- function(fullData, fname) {
  trial_data <- read.csv(paste("results/gabor",fname,sep="/",collapse=NULL),header=TRUE,fill=TRUE, stringsAsFactors=FALSE)
  #trial_data <- read.csv("results/gabor/cynthiaday1.csv", header=TRUE, fill=TRUE, stringsAsFactors=FALSE)
  trial_data <- filter(trial_data)
  dists <- getDist(trial_data)
  #medians
  medNoDist <- median( trial_data[dists$noDist,]$RT )
  medOneDist <- median( trial_data[dists$oneDist,]$RT)
  medTwoDist <- median( trial_data[dists$twoDist,]$RT)
  Acc <- calcAcc(trial_data, dists)
  
  cols <- c("No Distractor", "One Distractor", "Two Distractor")
  dfMedian <- data.frame(medians=c(medNoDist, medOneDist, medTwoDist), Type=cols)
  dfAcc <- data.frame(accuracy=c(Acc$noDistAcc,Acc$oneDistAcc,Acc$twoDistAcc), Type=cols)
  
  target <- trial_data$T[1]
  name <- trial_data$ID[1]
  day <- trial_data$day[1]
  
  p <- ggplot(data=dfMedian, aes(x=medians, y=Type, color=Type)) + geom_point(size=3) + coord_flip() +
    opts(title = paste(name,day,target, "Median response times",sep=" ",collapse=NULL) )
  ggsave(filename= paste("plots/",name,day,target, "MedianRT.jpg", sep="_", collapse=NULL), plot=p)
  
  p <- ggplot(data=trial_data, aes(x=TrialNum,y=RT,
                group=interaction(factor(NumDist),factor(D1),factor(D2)),
                color=interaction(factor(NumDist),factor(D1),factor(D2)))) +
                  geom_smooth() + guides(color=guide_legend(title="Distractors")) +
                    opts(title = paste(name,day,target, "Distractor response times", sep=" ",collapse=NULL))
  ggsave(filename=paste("plots/",name,day,target,"dist_RTs.jpg",sep="_",collapse=NULL), plot=p)
  
  p <- ggplot(data=trial_data, aes(x=factor(NumDist), y=RT,
                fill=interaction(factor(NumDist),factor(D1),factor(D2)),
                group=interaction(factor(NumDist),factor(D1),factor(D2)))) +
                  geom_jitter(aes(color=RT)) + geom_boxplot() +
                    guides(fill=guide_legend(title="Distractors"))+
                    opts(title = paste(name,day,target,"Distractor RTs",sep=" ",collapse=NULL))
  p + facet_grid(red ~.)
  ggsave(filename=paste("plots/",name,day,target,"dist_RTs_boxplot.jpg",sep="_",collapse=NULL), plot=p)
  
  p <- ggplot(dfAcc, aes(x=Type ,y=accuracy ,fill=Type)) + geom_bar() +
    opts(title=paste(name,day,target,"Accuracy",sep=" ",collapse=NULL) )
  ggsave(filename=paste("plots/",name,day,target,"accuracy.jpg",sep="_",collapse=NULL), plot=p)

  fullData <- writeData(fullData, trial_data)
  return(fullData)
}

run <- function() {
  fullData <- data.frame()
  for(name in files){
    fullData <- pilotStats(fullData, name)
  }
  write.table(data,file="results/fulldata.csv", sep=",")
}

run()
