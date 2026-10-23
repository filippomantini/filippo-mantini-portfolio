"""Seasonal archive: one unisex comparison, then a consistent lookbook gallery."""
def build_story(t,fig,group,intro,chapter):
 s=intro('01 / FW24/25 + SS24',t('ARCHIVIO<br>DI COLLEZIONE.','COLLECTION<br>ARCHIVE.'),t('FW24/25 e SS24 condividono la ricerca su volumi, denim e segni grafici. Il confronto unisex apre il racconto; la galleria raccoglie i look e i dettagli dei capi.','FW24/25 and SS24 share a study of volume, denim and graphic marks. A unisex comparison opens the story, followed by a gallery of looks and garment details.'))
 s+='<nav class="ca-jumps" aria-label="'+t('Capitoli della collezione','Collection chapters')+'"><a href="#fw24-25">FLUIDITY ↓</a><a href="#ss24">'+t('GALLERIA','GALLERY')+' ↓</a><a href="#graphic-system">GRAPHIC SYSTEM ↓</a></nav>'
 pair='<div class="pair ca-unisex-pair">'+fig('fw24ss24-fluidity-woman','Ragazza con felpa grigia C Logo e shorts grafici COLLAPSE, look unisex','Woman wearing the grey C Logo hoodie and graphic COLLAPSE shorts, unisex look','FLUIDITY / '+t('STESSO CAPO','SAME GARMENT'),True)+fig('fw24ss24-fluidity-man','Ragazzo con la stessa felpa grigia C Logo e gli stessi shorts grafici COLLAPSE','Man wearing the same grey C Logo hoodie and the same graphic COLLAPSE shorts','FLUIDITY / '+t('STESSO CAPO','SAME GARMENT'))+'</div>'
 s+=chapter('02 / UNISEX COLLECTION','FLUIDITY.',t('Fluidity esprime l’approccio unisex della collezione: i capi sono pensati per essere indossati da uomini e donne. La stessa felpa e gli stessi shorts sono mostrati su una ragazza e un ragazzo, per leggere come vestono su corpi diversi.','Fluidity reflects the collection’s unisex approach: the garments are designed to be worn by women and men. The same hoodie and shorts are shown on a woman and a man, revealing how they fit different bodies.'),pair,id='fw24-25')
 # Keep coherent rows: grey studio looks, warm studio looks, product views, details.
 items=[
 ('fw24ss24-01','Modello con felpa e pantaloni neri COLLAPSE su blocchi di cemento','Model in a black COLLAPSE hoodie and trousers on concrete blocks','LOOK / 01'),
 ('fw24ss24-02','Modella con completo denim COLLAPSE su blocchi di cemento','Model wearing a COLLAPSE denim set on concrete blocks','LOOK / 02'),
 ('fw24ss24-03','Look nero con polo COLLAPSE e cappello su base in cemento','Black COLLAPSE polo look with cap on concrete blocks','LOOK / 03'),
 ('fw24ss24-04','Modella con maglia grafica e pantaloni scuri nel set in studio','Model wearing a graphic top and dark trousers in the studio','LOOK / 04'),
 ('fw24ss24-14','Modello con camicia bianca a righe grafiche e denim scuro','Model in a white shirt with graphic lines and dark denim','LOOK / 05'),
 ('fw24ss24-15','Modella con T-shirt bianca e shorts grafici su blocchi in cemento','Model wearing a white T-shirt and graphic shorts on concrete blocks','LOOK / 06'),
 ('fw24ss24-17','Felpa grigia oversize con grande C chiara','Oversized grey hoodie with a large light C','LOOK / 07'),
 ('fw24ss24-21','Maglia verde e bianca con denim della collezione','Green and white shirt with collection denim','LOOK / 08'),
 ('fw24ss24-19','Canotta sportiva nera e arancione COLLAPSE','Black and orange COLLAPSE sports vest','PRODUCT / 01'),
 ('fw24ss24-20','Shorts sportivi neri e arancioni COLLAPSE','Black and orange COLLAPSE sports shorts','PRODUCT / 02'),
 ('fw24ss24-18','Shorts neri con segni grafici bianchi','Black shorts with white graphic marks','PRODUCT / 03'),
 ('fw24ss24-16','Dettaglio dei jeans a zampa con segni chiari','Flared denim trousers with light graphic marks','PRODUCT / 04'),
 ('fw24ss24-22','Shorts bianchi con disegno grafico a linee nere','White shorts with black line graphics','DETAIL / 01'),
 ('fw24ss24-10','Dettaglio della giacca denim con cuciture e segni grafici','Denim jacket detail with stitching and graphic marks','DETAIL / 02'),
 ('fw24ss24-11','Cappello nero e colletto con lettering COLLAPSE','Black cap and collar with COLLAPSE lettering','DETAIL / 03'),
 ('fw24ss24-06','Dettaglio della gonna denim con motivo COLLAPSE','Denim skirt detail with COLLAPSE motif','DETAIL / 04')]
 gallery='<div class="ca-lookbook">'+''.join(fig(*a,sizes='(max-width:600px) calc(50vw - 19px), calc(25vw - 22px)') for a in items)+'</div>'
 s+=chapter('03 / '+t('GALLERIA','GALLERY'),t('GALLERIA<br>DELLA COLLEZIONE.','COLLECTION<br>GALLERY.'),'',gallery,id='ss24')
 graphics=group([('fw24ss24-05','Composizione Denim Industry con moltiplicazione dei modelli in denim','Denim Industry composition repeating the denim campaign models','FW24/25 / DENIM INDUSTRY'),('fw24ss24-09','Copertina originale Fluidity con due modelli','Original Fluidity cover with two models','FW24/25 / FLUIDITY'),('fw24ss24-07','Griglia dei look e delle viste della collezione Fluidity','Grid of looks and views from the Fluidity collection','FW24/25 / COLLECTION GRID')],'trio')
 graphics+='<div style="margin-top:40px">'+group([('fw24ss24-12','Composizione originale Football Team con modelli in abbigliamento sportivo','Original Football Team composition with sportswear models','SS24 / FOOTBALL TEAM'),('fw24ss24-13','Composizione originale Off the Grid con camicie grafiche','Original Off the Grid composition with graphic shirts','SS24 / OFF THE GRID')])+'</div>'
 s+=chapter('04 / GRAPHIC SYSTEM',t('DAL LOOK<br>ALLA PUBBLICAZIONE.','FROM THE LOOK<br>TO PUBLICATION.'),t('Le composizioni originali organizzano i look in sequenze, griglie e immagini corali. FLUIDITY, DENIM INDUSTRY, OFF THE GRID e FOOTBALL TEAM rendono riconoscibili le diverse direzioni del progetto.','The original compositions organise looks into sequences, grids and group images. FLUIDITY, DENIM INDUSTRY, OFF THE GRID and FOOTBALL TEAM distinguish the project’s visual directions.'),graphics,True,id='graphic-system')+'</section>'
 return s
