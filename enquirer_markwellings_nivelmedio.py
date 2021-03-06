"""
@author: U{Nines Sanguino}
@version: 0.2
@since: 20Jun2015
"""

__version__ = '0.2'
__modified__ = '20Jun2015'
__author__ = 'Nines Sanguino'
from SPARQLWrapper import SPARQLWrapper, JSON, XML, RDF
import xml.dom.minidom



def getLocalLabel (instancia):
 
 	sparqlSesame = SPARQLWrapper("http://localhost:8080/openrdf-sesame/repositories/SocialNetwork",  returnFormat=JSON)
	queryString = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX sn:  <http://ciff.curso2015/ontologies/owl/socialNetwork#> SELECT ?label WHERE { sn:" + instancia + " rdfs:label ?label }"
	sparqlSesame.setQuery(queryString)
	sparqlSesame.setReturnFormat(JSON)
	query   = sparqlSesame.query()
	results = query.convert()
	devolver = []
	for result in results["results"]["bindings"]:
		label = result["label"]["value"]
		if 'xml:lang' in result["label"]:
			lang = result["label"]["xml:lang"]
		else:
			lang = None
		print "The label: " + label
		if 'xml:lang' in result["label"]:
			print "The lang: " + lang
		devolver.append((label, lang))
	return devolver


	
def getDBpediaResource (label, lang, endpoint):

	sparqlDBPedia = SPARQLWrapper(endpoint)
	if (lang):
		queryString = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX dbo:	<http://dbpedia.org/ontology/> SELECT ?s ?abs WHERE  { ?s rdfs:label \"" + label + "\"@" +lang + " . ?s rdf:type foaf:Person.?s dbo:abstract ?abs}" 
	else:
		queryString = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX dbo:	<http://dbpedia.org/ontology/> SELECT ?s ?abs WHERE  { ?s rdfs:label \"" + label + "\" . ?s rdf:type foaf:Person.?s dbo:abstract ?abs}" 
	
	sparqlDBPedia.setQuery(queryString)
	sparqlDBPedia.setReturnFormat(JSON)
	query   = sparqlDBPedia.query()
	results = query.convert()
	for result in results["results"]["bindings"]:
		resource = result["s"]["value"]
		abstract = result["abs"]["value"] 
		print "The resource: " + resource
		print "Please see Alicia Keys' abstract: " + abstract

def getLinkedmdbResource (label, lang, endpoint):

   sparqlLinkedmdb = SPARQLWrapper(endpoint)
   
   if (lang):
      queryString = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX dc: <http://purl.org/dc/terms/> PREFIX movie: <http://data.linkedmdb.org/resource/movie/> SELECT ?s ?date ?time WHERE { ?s rdfs:label \"" + label + "\"@" +lang + ".?s dc:date ?date.?s movie:runtime ?time } " 
   
   else:
      queryString = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX dc: <http://purl.org/dc/terms/> PREFIX movie: <http://data.linkedmdb.org/resource/movie/> SELECT ?s ?date ?time WHERE { ?s rdfs:label \"" + label + "\" .?s dc:date ?date.?s movie:runtime ?time }   " 
   
   sparqlLinkedmdb.setQuery(queryString)
   sparqlLinkedmdb.setReturnFormat(JSON)
   query   = sparqlLinkedmdb.query()
   results = query.convert()
   print
   for result in results["results"]["bindings"]: 
      resource = result["s"]["value"] 
      datum	= result["date"]["value"]
      zeit = result["time"]["value"]
      print "The resource: " + resource 
      print "The release date. " + datum
      print "The runtime is(in minutes): " +zeit

def getWebenemasunoResource (label, lang, endpoint):

   sparqlWebenemasuno = SPARQLWrapper(endpoint)

   if (lang):
      queryString = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX sioc: <http://rdfs.org/sioc/ns#> SELECT ?s   ?date ?creator WHERE { ?s sioc:title \"" + label + "\"@" +lang + ".?s sioc:created_at ?date.?s sioc:has_creator ?creator} " 
   else:
      queryString = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX sioc: <http://rdfs.org/sioc/ns#>  SELECT ?s  ?date ?creator WHERE { ?s sioc:title \"" + label + "\".?s sioc:created_at ?date.?s sioc:has_creator ?creator} "
      
   sparqlWebenemasuno.setQuery(queryString)
   sparqlWebenemasuno.setReturnFormat(JSON)
   query   = sparqlWebenemasuno.query()
   results = query.convert()
   print
   for result in results["results"]["bindings"]: 
      resource = result["s"]["value"] 
      datum = result["date"]["value"]
      author = result["creator"]["value"]
      print "The resource: " + resource 
      print "The date: " + datum
      print "Written by: " + author
		

if __name__ == '__main__':

   # getLocalLabel devuelve una lista con todas las instancias que haya con sus label y lang
   # y luego se hace la llamada al repositorio externo para enriquecer cada combinacion de label-lang recibida
   lista = getLocalLabel("instancia1");
   print lista
   endpoint = 'http://dbpedia.org/sparql';
   for result in lista:
      (label, lang) = result
      resource = getDBpediaResource (label, lang, endpoint);

   print "\n---------------------\n"


   # Descomentar las siguientes lineas y modificar en cada 
   lista = getLocalLabel("instancia3");
   print lista
   endpoint = 'http://data.linkedmdb.org/sparql';
   for result in lista:
      (label, lang) = result
      resource = getLinkedmdbResource (label, lang, endpoint);

   print "\n---------------------\n"

   lista = getLocalLabel("instancia4");
   print lista
   endpoint = 'http://webenemasuno.linkeddata.es/sparql';
   for result in lista:
      (label, lang) = result
      resource = getWebenemasunoResource (label, lang, endpoint);
