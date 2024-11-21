package org.example;

import java.io.File;
import java.net.URL;
import java.util.List;

import org.openrdf.OpenRDFException;
import org.openrdf.model.Statement;
import org.openrdf.model.Value;
import org.openrdf.query.BindingSet;
import org.openrdf.query.GraphQueryResult;
import org.openrdf.query.Query;
import org.openrdf.query.QueryLanguage;
import org.openrdf.query.QueryResult;
import org.openrdf.query.TupleQuery;
import org.openrdf.query.TupleQueryResult;
import org.openrdf.query.resultio.sparqlxml.SPARQLResultsXMLWriter;
import org.openrdf.repository.Repository;
import org.openrdf.repository.RepositoryConnection;
import org.openrdf.repository.RepositoryException;
import org.openrdf.repository.sail.SailRepository;
import org.openrdf.rio.RDFFormat;
import org.openrdf.sail.inferencer.fc.ForwardChainingRDFSInferencer;
import org.openrdf.sail.memory.MemoryStore;

public class TestWithRDFS {

	//static final String inputDataURL  = "http://localhost:8080/pms509/rdf-data/culture_data.rdf";
	//static final String inputSchemaURL = "http://localhost:8080/pms509/rdf-data/culture.rdfs";
	
	static final String inputDataURL  = "file:///Users/gstam/Dropbox/Documents/COURSES/PMS 509/sesame-tutorial-new/culture_data.rdf";
	static final String inputSchemaURL = "file:///Users/gstam/Dropbox/Documents/COURSES/PMS 509/sesame-tutorial-new/culture.rdfs";
	static final String inputData2  = "file:///C:/Users/kosta/OneDrive/Υπολογιστής/Mathimata_sxolhs/Texnologies Gnwsewn/sesame-tutorial-new/schemaorg-current-https.nt";

	
	public static void main(String[] args) {

		try {
			//Create a new main memory repository 
			MemoryStore store = new MemoryStore();
			ForwardChainingRDFSInferencer inferencer = new ForwardChainingRDFSInferencer(store);
			
			//Repository repo = new SailRepository(store);
			Repository repo = new SailRepository(inferencer);
			repo.initialize();

			//Store files (one local and one available through http)	
			URL data = new URL(inputData2);
			//URL schema = new URL(inputSchemaURL);
			String fileBaseURI = "http://zoi.gr/culture#";
			RDFFormat fileRDFFormat = RDFFormat.NTRIPLES;
			RepositoryConnection con = repo.getConnection();
			
			//store the files
			con.add(data, null, fileRDFFormat);
			//con.add(schema, fileBaseURI, fileRDFFormat);
	
			System.out.println("Repository loaded");

			//Sesame supports:
			//Tuple queries: queries that produce sets of value tuples.
			//Graph queries: queries that produce RDF graphs
			//Boolean queries: true/false queries			
			
			//Evaluate a SPARQL tuple query
			String queryString1 = 
				" PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" +
				" PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \n" +
				" PREFIX gag: <http://geo.linkedopendata.gr/gag/ontology/>\n" +
				" SELECT ?x \n" +
				" WHERE { ?x rdf:type gag:Διοικητική_Μονάδα . }LIMIT 10";
					
			String queryString2 = "prefix ns:   <http://zoi.gr/culture#>" +
				" PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" +
			 	" SELECT ?x " +
			 	" WHERE { ?x  rdf:type  ns:Artist }" ;
				        
			String queryString3 = "prefix ns:   <http://zoi.gr/culture#>" +
							" prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" +
							" prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>" +
							"SELECT ?x WHERE { ?x  rdf:type  rdfs:Class }";
				        
			String queryString4 = "prefix ns:   <http://zoi.gr/culture#>" +
							" prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" +
							" SELECT ?x " +
							" WHERE { ?x  rdf:type  rdf:Property }";
				        

			String queryString5 = "prefix ns:   <http://zoi.gr/culture#>" +
				        " SELECT ?x ?y " +
				        " WHERE { ?x  ns:creates  ?y } ";
				        
			String queryString6 = "prefix ns:   <http://zoi.gr/culture#>" +
				        " SELECT ?x ?y " +
				        " WHERE { ?x  ns:creates  ?y . " +
				        " ?y ns:exhibited <http://www.louvre.fr/>} ";
				                
			String queryString7 = "prefix ns:   <http://zoi.gr/culture#>" +
				        		" prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" +
				        " SELECT ?x WHERE { ?x  ns:created  ?y " +
				        " FILTER (?y < 1990) . " +
				        " ?x rdf:type ns:Artifact} ";
				        
			String queryString8 = "prefix ns:   <http://zoi.gr/culture#>" +
						" prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" +
						" SELECT ?x ?y " +
						" WHERE { ?x  ns:created  ?y " +
						" FILTER (?y < 1990) . " +
						" ?x rdf:type ns:Sculpture} ";
					
			/*
			  Q1:Find all subclasses of class CollegeOrUniversity (note that http://schema.org/ prefers to
				 use the equivalent term “type” for “class”).
			 */
				 
			String queryString9 = " PREFIX org: <https://schema.org/>\n" +
						  "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" +
						  "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" +
						  "SELECT ?x \n" +
						  "WHERE {?x rdfs:Class/rdfs:subClassOf* org:CollegeOrUniversity}";
			
			/*
			 Q2:Find all the superclasses of class CollegeOrUniversity. 
			 
			*/
			
			String queryString10 = " PREFIX org: <https://schema.org/>\n" +
					  "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" +
					  "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" +
					  "SELECT ?x \n" +
					  "WHERE {org:CollegeOrUniversity rdfs:subClassOf* ?x}";
			
			/*
			 Q3:Find all properties defined for the class CollegeOrUniversity together with all the
				properties inherited by its superclasses. 
			*/
			
			String queryString11 = " PREFIX org: <https://schema.org/>\n" +
					  "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" +
					  "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" +
					  "SELECT DISTINCT ?p ?pr_sup\n" +
					  "WHERE { "+
					  "			{org:CollegeOrUniversity ?p ?x .\n" +
					  "      	} UNION"+
					  "         {org:CollegeOrUniversity rdfs:subClassOf* ?x .\n"+
					  "          ?x ?pr_sup ?val .\n"+
					  "         }"+
					  "      }";

			
			/*
			 Q4:Find all classes that are subclasses of class Thing and are found in at most 2 levels of
				subclass relationships away from Thing.
 
			*/
			
			String queryString12 = " PREFIX org: <https://schema.org/>\n" +
					  "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" +
					  "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" +
					  "SELECT DISTINCT ?x_1 ?x_2\n" +
					  "WHERE { "+
					  "			?x_1 rdfs:subClassOf org:Thing .\n" +
					  "			?x_2 rdfs:subClassOf ?x_1 .\n"+			
					  "      }";

			
			
			
			String queryString = queryString12;
			TupleQuery tupleQuery = con.prepareTupleQuery(QueryLanguage.SPARQL, queryString);
			TupleQueryResult result = tupleQuery.evaluate();
			System.out.println("Query:\n" + queryString);
					
			try {
				//iterate the result set
				while (result.hasNext()) {
					BindingSet bindingSet = result.next();
					System.out.println(bindingSet.toString());
				}

				
			} finally {
						result.close();
			}
				
		}
		catch (Exception e) {
			// handle exception
			e.printStackTrace();
		}
	}
}
