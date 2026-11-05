const {readFileSync}=require('node:fs');
const vm=require('node:vm');
const assert=require('node:assert/strict');
const elements=new Map();
function element(){return {innerHTML:'',textContent:'',value:'',style:{},classList:{toggle(){}},dataset:{}};}
const listeners={};const memory={};
const context=vm.createContext({console,Blob,URL,setTimeout:()=>0,clearTimeout(){},confirm:()=>true,location:{hash:'#overview'},localStorage:{getItem:k=>memory[k]??null,setItem:(k,v)=>memory[k]=v},document:{querySelector(s){if(!elements.has(s))elements.set(s,element());return elements.get(s);},querySelectorAll(){return [];},addEventListener:(k,f)=>listeners[k]=f,createElement:()=>({click(){}})},window:{addEventListener(){},scrollTo(){},print(){}}});
function run(s){return vm.runInContext(s,context);}
for(const f of ['content.js','app.js'])run(readFileSync('dist/'+f,'utf8'));
const click=script=>run(`documentClickTarget=${script};`);
context.documentClickTarget=null;
function press(id,dataset={}){listeners.click({target:{closest:()=>({id,dataset})}});}
assert.match(elements.get('#main').innerHTML,/Your coding comeback/);
assert.equal(run('LESSONS.length'),13);
for(let i=1;i<=13;i++){
 run(`location.hash='#learn/${i}';render()`);
 assert.match(elements.get('#main').innerHTML,/Your notes &amp; sticky points|Your notes & sticky points/);
}
run("location.hash='#learn/1';render()");press('complete');assert.equal(run("state.done.includes('1')"),true);
press('save-topic');assert.equal(run("state.saved.includes('1')"),true);
listeners.input({target:{id:'topic-note',value:'A reference, not a copy. <script>unsafe</script>'}});
run('render()');assert.match(elements.get('#main').innerHTML,/&lt;script&gt;/);
assert.match(memory['prep-studio-v1'],/A reference/);
run("filter='saved';query='';location.hash='#learn';render()");assert.match(elements.get('#main').innerHTML,/Variables/);assert.ok(!elements.get('#main').innerHTML.includes('data-lesson="2"'));
listeners.input({target:{id:'search',value:'nonexistent-987654'}});assert.match(elements.get('#lesson-results').innerHTML,/No topics match/);
run("location.hash='#recall';render()");assert.match(elements.get('#main').innerHTML,/Reveal explanation/);press('reveal');assert.match(elements.get('#main').innerHTML,/Both names refer/);press('know');assert.equal(run('state.known.length'),1);press('next-card');assert.equal(run('cardIndex'),1);assert.equal(run('revealed'),false);
run("location.hash='#plan';render()");listeners.change({target:{dataset:{day:'0'}}});assert.equal(run('state.days[0]'),0);
assert.equal(run('cleanState({done:["1","1","999"],notes:{"1":"ok"}}).done.length'),1);
// Reload the application into a fresh context with the same backing storage.
const reloaded=vm.createContext({...context});
for(const f of ['content.js','app.js'])vm.runInContext(readFileSync('dist/'+f,'utf8'),reloaded);
assert.equal(vm.runInContext('state.done.includes("1") && state.saved.includes("1") && state.days.includes(0)',reloaded),true);
console.log('Verified all 13 lessons, search/filter, completion, saved topics, escaped notes, persistence/reload, roadmap checks, and recall controls.');
