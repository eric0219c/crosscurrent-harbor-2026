import http from 'node:http';
import worker from './harbor-worker.js';
import { localDatabase } from './local-db.mjs';
const DB = localDatabase();
const server = http.createServer(async(req,res)=>{try{const parts=[];let bytes=0;for await(const chunk of req){bytes+=chunk.length;if(bytes>4096){res.writeHead(413);res.end();return}parts.push(chunk)}const url='http://127.0.0.1:8792'+req.url;const request=new Request(url,{method:req.method,headers:req.headers,...(req.method!=='GET'&&req.method!=='HEAD'?{body:Buffer.concat(parts)}:{})});const result=await worker.fetch(request,{DB},{});res.writeHead(result.status,Object.fromEntries(result.headers));res.end(Buffer.from(await result.arrayBuffer()))}catch{res.writeHead(500);res.end('Preview error')}});
server.listen(8792,'127.0.0.1',()=>console.log('Crosscurrent Harbor preview: http://127.0.0.1:8792'));
process.on('SIGTERM',()=>server.close(()=>{DB.close();process.exit(0)}));
