import{m as o,c as r,C as a}from"./index.de5afc43.js";import{g as l}from"./userscore.78b9c477.js";import{e as u}from"./index.1cf73b05.js";import"./echarts.128204f2.js";window.Alpine=o;o.data("UserGraphs",()=>({solves:null,fails:null,awards:null,solveCount:0,failCount:0,awardCount:0,getSolvePercentage(){return(this.solveCount/(this.solveCount+this.failCount)*100).toFixed(2)},getFailPercentage(){return(this.failCount/(this.solveCount+this.failCount)*100).toFixed(2)},getCategoryBreakdown(){const e=[],s={};this.solves.data.map(t=>{e.push(t.challenge.category)}),e.forEach(t=>{t in s?s[t]+=1:s[t]=1});const i=[];for(const t in s){const n=Number(s[t]/e.length*100).toFixed(2);i.push({name:t,count:s[t],color:r(t),percent:n})}return i},async init(){this.solves=await a.pages.users.userSolves(window.USER.id),this.fails=await a.pages.users.userFails(window.USER.id),this.awards=await a.pages.users.userAwards(window.USER.id),this.solveCount=this.solves.meta.count,this.failCount=this.fails.meta.count,this.awardCount=this.awards.meta.count;let e=window.userScoreGraphChartOptions;u(this.$refs.scoregraph,l(window.USER.id,window.USER.name,this.solves.data,this.awards.data,e))}}));o.start();
