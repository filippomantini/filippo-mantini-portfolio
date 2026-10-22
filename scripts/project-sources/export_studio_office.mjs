// Render the app's original floor plan without connecting or starting the app.
import {createOfficeScene} from '../../public/assets/studio/workers-src/immersive-office.js';
import {writeFileSync} from 'node:fs';
const agents=JSON.parse(process.argv[2]);
const node=()=>({dataset:{},setAttribute(){},querySelector(){return {textContent:''}}});
const container={innerHTML:'',querySelectorAll:()=>[],querySelector:node,addEventListener(){}};
createOfficeScene(container,{officeId:'design',agents:agents.filter(a=>a.offices.includes('design')),snapshot:{projects:[],tasks:[],runs:[]},onSelect(){},onZone(){}});
writeFileSync(new URL('./studio-office-default.svg',import.meta.url),container.innerHTML);
