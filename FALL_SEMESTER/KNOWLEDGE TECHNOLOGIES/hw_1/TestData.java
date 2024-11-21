package org.example;

import java.net.URL;
import java.util.List;

import org.openrdf.OpenRDFException;
import org.openrdf.model.Value;
import org.openrdf.query.BindingSet;
import org.openrdf.query.QueryLanguage;
import org.openrdf.query.TupleQuery;
import org.openrdf.query.TupleQueryResult;
import org.openrdf.query.resultio.sparqlxml.SPARQLResultsXMLWriter;
import org.openrdf.repository.Repository;
import org.openrdf.repository.RepositoryConnection;
import org.openrdf.repository.RepositoryException;
import org.openrdf.repository.sail.SailRepository;
import org.openrdf.rio.RDFFormat;
import org.openrdf.sail.memory.MemoryStore;

public class TestData {

	static final String inputData  = "http://localhost:8080/pms509/rdf-data/culture_data.rdf";
	static final String dataUrlString = "http://localhost:8080/pms509/rdf-data/data-2-100.rdf";
	static final String inputData2  = "file:///C:/Users/kosta/OneDrive/Υπολογιστής/Mathimata_sxolhs/Texnologies Gnwsewn/Kallikratis-Geonames.nt";
	
	public static void main(String[] args) {

		try {
			//Create a new main memory repository 
			MemoryStore store = new MemoryStore();
			Repository repo = new SailRepository(store);
			repo.initialize();

			//Store file
			try {
				//URL file = new URL(inputData);
				//String fileBaseURI = "http://zoi.gr/culture#";
				//RDFFormat fileRDFFormat = RDFFormat.RDFXML;
				
				URL file = new URL(inputData2);
				String fileBaseURI = "http://geo.linkedopendata.gr/gag/ontology/";
				RDFFormat fileRDFFormat = RDFFormat.NTRIPLES;
		
				RepositoryConnection con = repo.getConnection();
				try {
					//store the file
					con.add(file, fileBaseURI, fileRDFFormat);
					System.out.println("Repository loaded");
					
					//store file from url
					//URL url = new URL(dataUrlString);
					//con.add(url, null, fileRDFFormat);
				}
				finally {
					con.close();
				}
			}
			catch (OpenRDFException e) {
				e.printStackTrace();
			}
			catch (java.io.IOException e) {
				// handle io exception
				e.printStackTrace();
			}


			//Sesame supports:
			//Tuple queries: queries that produce sets of value tuples.
			//Graph queries: queries that produce RDF graphs
			//Boolean queries: true/false queries			
			
			//Evaluate a SPARQL tuple query
			try {
				RepositoryConnection con = repo.getConnection();
				try {
					String queryString1 = "prefix ns:   <http://zoi.gr/culture#>" +
			        " SELECT ?x ?y " +
			        " WHERE { ?x  ns:paints  ?y } ";
	        
			        String queryString2 = "prefix ns:   <http://zoi.gr/culture#>" +
			        " SELECT ?x ?y " +
			        " WHERE { ?x  ns:paints  ?y . " +
			        "   ?y ns:exhibited <http://www.louvre.fr/> .} ";
			        
			        String queryString3 = "prefix ns:   <http://zoi.gr/culture#>" +
			        " SELECT ?x " +
			        " WHERE { ?x  ns:first_name  \"August\" . } ";
			        
			        String queryString3b = "prefix ns:   <http://zoi.gr/culture#>" +
			        " SELECT ?y " +
			        " WHERE { ?x  ns:first_name  \"August\" ." +
			        "	?x ns:last_name ?y . } ";
			        
			        String queryString4 = "prefix ns:   <http://zoi.gr/culture#>" +
			        " SELECT ?x ?y " +
			        " WHERE { ?x  ns:first_name  ?y" +
			        " FILTER regex(str(?x), \"rodin\") } ";
			        
			        String queryString5 = "prefix ns:   <http://zoi.gr/culture#>" +
			        " SELECT ?x ?y " +
			        " WHERE { ?x  ns:created  ?y " +
			        " FILTER (?y < 1990) } ";
			        
			        String queryString6 = "prefix ns:   <http://zoi.gr/culture#>" +
			        " SELECT ?x ?z ?w " +
			        " WHERE { ?x   ns:paints  ?y ." +
			        " OPTIONAL {?x ns:first_name ?z ." +
			        "			?x ns:last_name ?w}} ";
			        
			        String queryString7 = "prefix ns:   <http://zoi.gr/culture#>" +
			        " SELECT ?x ?y " +
			        " WHERE { {?x  ns:sculpts  ?y }" +
			        " UNION {?x ns:paints ?y} } ";
			        
			        String queryrrrr= "prefix ns:   <http://cgi.di.uoa.gr/~ys02/rdf/schema-2.rdf#>" +
					" PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" +
				 	" SELECT ?x " +
				 	" WHERE { ?x  rdf:type  ns:Class0 }" ;
			        
			        String queryString8= "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n" + 
			        		"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" + 
			        		"PREFIX strdf: <http://strdf.di.uoa.gr/ontology#>\n" + 
			        		"PREFIX gag: <http://geo.linkedopendata.gr/gag/ontology/>\n" + 
			        		"PREFIX owl: <http://www.w3.org/2002/07/owl#>\n" + 
			        		"\n" + 
			        		"SELECT ?test ?p ?o \n" + 
			        		"WHERE \n" + 
			        		"{\n" + 
			        		"       ?m rdf:type gag:Δήμος .\n" + 
			        		"       ?m owl:sameAs ?test .\n" + 
			        		"       ?test ?p  ?o .\n" + 
			        		"}limit 100";
			        
			        String queryString9= "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n" + 
			        		"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" + 
			        		"PREFIX strdf: <http://strdf.di.uoa.gr/ontology#>\n" + 
			        		"PREFIX gag: <http://geo.linkedopendata.gr/gag/ontology/>\n" + 
			        		"PREFIX owl: <http://www.w3.org/2002/07/owl#>\n" + 
			        		"\n" + 
			        		"SELECT ?municipalityName \n" + 
			        		"WHERE \n" + 
			        		"{\n" + 
			        		"       ?m rdf:type gag:Δήμος .\n" + 
			        		"       ?m gag:έχει_επίσημο_όνομα ?municipalityName .\n" + 
			        		"}";
			        

					// Q1: Give the official name and population of each municipality (δήμος) of Greece.
			        
			        String queryString10= "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n" + 
			        		"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" + 
			        		"PREFIX strdf: <http://strdf.di.uoa.gr/ontology#>\n" + 
			        		"PREFIX gag: <http://geo.linkedopendata.gr/gag/ontology/>\n" + 
			        		"PREFIX owl: <http://www.w3.org/2002/07/owl#>\n" + 
			        		"\n" + 
			        		"SELECT ?municipalityName ?population\n" + 
			        		"WHERE \n" + 
			        		"{\n" + 
			        		"       ?m rdf:type gag:Δήμος .\n" + 
			        		"       ?m gag:έχει_επίσημο_όνομα ?municipalityName .\n" +
			        		"		?m gag:έχει_πληθυσμό ?population\n" +
			        		"}";
			        
			        /* Q2: For each region (περιφέρεια) of Greece, give its official name, the official name of each
						regional unit (περιφερειακή ενότητα) that belongs to it, and the official name of each
						municipality (δήμος) in this regional unit. Organize your answer by region, regional unit
						and municipality. 
			         */
			        String queryString11= "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n" + 
			        		"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" + 
			        		"PREFIX strdf: <http://strdf.di.uoa.gr/ontology#>\n" + 
			        		"PREFIX gag: <http://geo.linkedopendata.gr/gag/ontology/>\n" + 
			        		"PREFIX owl: <http://www.w3.org/2002/07/owl#>\n" + 
			        		"\n" + 
			        		"SELECT ?region ?regional_unit ?municipality  \n" + 
			        		"WHERE \n" + 
			        		"{\n" + 
			        		"       ?m rdf:type gag:Δήμος .\n" +
			        		"		?m gag:έχει_επίσημο_όνομα ?municipality .\n"+		
			        		"       ?m gag:ανήκει_σε ?reg_un .\n" +
			        		"		?reg_un gag:έχει_επίσημο_όνομα ?regional_unit .\n" +
			        		"		?reg_un gag:ανήκει_σε ?reg .\n"+
			        		"		?reg gag:έχει_επίσημο_όνομα ?region .\n"+	
			        		"}";
			        /*
			           Q3: For each municipality of the region Peloponnese with population more than 5,000 people,
					   give its official name, its population, and the regional unit it belongs to. Organize your
					   answer by municipality and regional unit.
			         */
			        
			        String queryString12= "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n" + 
			        		"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" + 
			        		"PREFIX strdf: <http://strdf.di.uoa.gr/ontology#>\n" + 
			        		"PREFIX gag: <http://geo.linkedopendata.gr/gag/ontology/>\n" + 
			        		"PREFIX owl: <http://www.w3.org/2002/07/owl#>\n" + 
			        		"\n" + 
			        		"SELECT ?municipality  ?regional_unit\n" + 
			        		"WHERE \n" + 
			        		"{\n" + 
			        		"       ?m rdf:type gag:Δήμος .\n" +
			        		"		?m gag:έχει_επίσημο_όνομα ?municipality .\n"+		
			        		"       ?m gag:ανήκει_σε ?reg_un .\n" +
			        		"		?m gag:έχει_πληθυσμό ?population .\n" +
			        		"		?reg_un gag:έχει_επίσημο_όνομα ?regional_unit .\n"+
			        		"		?reg_un gag:ανήκει_σε ?reg .\n" +
			        		"		?reg gag:έχει_επίσημο_όνομα 'ΠΕΡΙΦΕΡΕΙΑ ΠΕΛΟΠΟΝΝΗΣΟΥ'.\n"+
			        		"		FILTER(?population > 5000)."+		
			        		"}";
			        
			        /*
			            Q4: For each municipality of Peloponnese for which we have no seat (έδρα) information in
						the dataset, give its official name.
			         */
			        
			        String queryString13= "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n" + 
			        		"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" + 
			        		"PREFIX strdf: <http://strdf.di.uoa.gr/ontology#>\n" + 
			        		"PREFIX gag: <http://geo.linkedopendata.gr/gag/ontology/>\n" + 
			        		"PREFIX owl: <http://www.w3.org/2002/07/owl#>\n" + 
			        		"\n" + 
			        		"SELECT ?municipality ?seat\n" + 
			        		"WHERE \n" + 
			        		"{\n" + 
			        		"       ?m rdf:type gag:Δήμος .\n" +
			        		"		?m gag:έχει_επίσημο_όνομα ?municipality .\n"+
			        		"		OPTIONAL{?m gag:έχει_έδρα ?seat} .\n"+
			        		"       ?m gag:ανήκει_σε ?reg_un .\n" +
			        		"		?reg_un gag:ανήκει_σε ?reg .\n" +
			        		"		?reg gag:έχει_επίσημο_όνομα 'ΠΕΡΙΦΕΡΕΙΑ ΠΕΛΟΠΟΝΝΗΣΟΥ'.\n"+
			        		"		FILTER(!bound(?seat)) .\n"+
			        		"}";
			        
			        
			        /*
			         	Q5:For each municipality of Peloponnese, give its official name and all the administrative
						divisions of Greece that it belongs to according to Kallikratis. Your query should be the
						simplest one possible, and it should not use any explicit knowledge of how many levels
						of administration are imposed by Kallikratis
			         */
			        
			        	        

			        String queryString14= "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n" + 
			        		"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" + 
			        		"PREFIX strdf: <http://strdf.di.uoa.gr/ontology#>\n" + 
			        		"PREFIX gag: <http://geo.linkedopendata.gr/gag/ontology/>\n" + 
			        		"PREFIX owl: <http://www.w3.org/2002/07/owl#>\n" + 
			        		"\n" + 
			        		"SELECT ?name ?type ?ab_type\n" + 
			        		"WHERE \n" + 
			        		"{\n" +
			        		" ?x rdf:type gag:Δήμος . \n"+ // Start from municipality
			        		" ?x gag:έχει_επίσημο_όνομα ?name . \n"+ //Take name
			        		" ?x gag:ανήκει_σε* ?div . \n"+ // Take all above divisions
			        		" ?div rdf:type ?type . \n"+ // Take type of division
			        		" ?div gag:έχει_επίσημο_όνομα 'ΠΕΡΙΦΕΡΕΙΑ ΠΕΛΟΠΟΝΝΗΣΟΥ' . \n"+ // Filter
			        		" ?x gag:ανήκει_σε* ?ab_div . \n"+
			        		" ?ab_div rdf:type ?ab_type . \n"+
			        		"} GROUP BY ?name ?type ?ab_type";
			        
			        
			        /*
			         	Q6:For each region of Greece, give its official name, how many municipalities belong to it,
						the official name of each regional unit (περιφερειακή ενότητα) that belongs to it, and how
						many municipalities belong to that regional unit.
			         */
			        
			        
			        
			        String queryString15= "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n" + 
			        		"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" + 
			        		"PREFIX strdf: <http://strdf.di.uoa.gr/ontology#>\n" + 
			        		"PREFIX gag: <http://geo.linkedopendata.gr/gag/ontology/>\n" + 
			        		"PREFIX owl: <http://www.w3.org/2002/07/owl#>\n" + 
			        		"\n" + 
			        		"SELECT ?region_name ?total_m ?unit ?total_reg_un WHERE\n"+
			        		"{\n"+
			        		"   {SELECT ?region_name (COUNT(?municipality) AS ?total_m)\n"+
			        		"    WHERE\n"+
			        		"    {\n"+
			        		"        ?m rdf:type gag:Δήμος .\n "+
			        		"		 ?m gag:έχει_επίσημο_όνομα ?municipality .\n"+
			        		"        ?m gag:ανήκει_σε ?reg_un .\n"+
			        		"        ?reg_un gag:ανήκει_σε ?region .\n"+
			        		"        ?region gag:έχει_επίσημο_όνομα ?region_name .\n"+
			        		"    } GROUP BY ?region_name"+
			        		"   }"+
			        		"	{SELECT  ?unit (COUNT(?municipality) AS ?total_reg_un)"+
			        		"		WHERE \n" + 
			        		"		{ ?m rdf:type gag:Δήμος .\n "+
			        		"  		?m gag:έχει_επίσημο_όνομα ?municipality .\n"+
			        		"  		?m gag:ανήκει_σε ?reg_un .\n"+
			        		"  		?reg_un gag:έχει_επίσημο_όνομα ?unit .\n"+
			        		"		} GROUP BY ?unit"+
			        		"	}"+
			        		"} GROUP BY ?region_name ?total_m ?unit ?total_reg_un ORDER BY ?region_name ?total_m ?unit ?total_reg_un";
			        		
			        
			        
			        /*
			         Q7:Check the consistency of the dataset regarding stated populations: the sum of the
						populations of all administrative units A of level L must be equal to the population of the
						administrative unit B of level L+1 to which all administrative units A belong to. (You
						have to write one query only.)
			         */
			        
			        
			        String queryString16= "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n" + 
			        		"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" + 
			        		"PREFIX strdf: <http://strdf.di.uoa.gr/ontology#>\n" + 
			        		"PREFIX gag: <http://geo.linkedopendata.gr/gag/ontology/>\n" + 
			        		"PREFIX owl: <http://www.w3.org/2002/07/owl#>\n" + 
			        		"\n" + 
			        		"SELECT ?type_x (SUM(?x_pop) AS ?pop_x) ?type_y ?y_pop\n" + 
			        		"WHERE \n" + 
			        		"{\n" +
			        		" ?x rdf:type gag:Δημοτική_Ενότητα .\n"+
			        		" ?x gag:ανήκει_σε* ?y .\n"+
			        		" ?x rdf:type ?type_x .\n"+ // ?type_x always equals to 'Δημοτική_Ενότητα'
			        		" ?y rdf:type ?type_y .\n"+ // Gets all the values of the administrative units (Δήμος, Δημοτική ενότητα etc)
			        		" ?x gag:έχει_πληθυσμό ?x_pop .\n"+
			        		" ?y gag:έχει_πληθυσμό ?y_pop . \n"+
			        		"} GROUP BY ?type_x ?x_pop ?type_y ?y_pop ORDER BY ?y_pop";
			        
			        
			        /*
			         Q8:Give the decentralized administrations (αποκεντρωμένες διοικήσεις) of Greece that
						consist of more than two regional units. (You cannot use SPARQL 1.1 aggregate
						operators to express this query.)
			         */
			        
			        String queryString17= "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n" + 
			        		"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" + 
			        		"PREFIX strdf: <http://strdf.di.uoa.gr/ontology#>\n" + 
			        		"PREFIX gag: <http://geo.linkedopendata.gr/gag/ontology/>\n" + 
			        		"PREFIX owl: <http://www.w3.org/2002/07/owl#>\n" + 
			        		"\n" + 
			        		"SELECT DISTINCT ?dec_name\n" + 
			        		"WHERE \n" + 
			        		"{\n" +
			        		" ?x rdf:type gag:Περιφερειακή_Ενότητα . \n"+ 
			        		" ?x gag:ανήκει_σε ?region . \n"+ 
			        		" ?region gag:ανήκει_σε ?dec .\n"+
			        		" ?y rdf:type gag:Περιφερειακή_Ενότητα . \n"+
			        		" ?y gag:ανήκει_σε ?region_2 . \n"+
			        		" ?region_2 gag:ανήκει_σε ?dec .\n"+
			        		" ?z rdf:type gag:Περιφερειακή_Ενότητα . \n"+
			        		" ?z gag:ανήκει_σε ?region_3 . \n"+
			        		" ?region_3 gag:ανήκει_σε ?dec .\n"+
			        		" ?dec gag:έχει_επίσημο_όνομα ?dec_name .\n"+
			        		" FILTER((?x != ?y) && (?y != ?z) && (?x != ?z)) .\n"+
			        		"}";
			        
			        
			        String queryString = queryString17;
					TupleQuery tupleQuery = con.prepareTupleQuery(QueryLanguage.SPARQL, queryString);
					TupleQueryResult result = tupleQuery.evaluate();
					System.out.println("Query:\n" + queryString);
					try {
						//iterate the result set
						//result = tupleQuery.evaluate();
						while (result.hasNext()) {
							BindingSet bindingSet = result.next();
							System.out.println(bindingSet.toString());
							
							//Value valueOfX = bindingSet.getValue("x");
							//Value valueOfY = bindingSet.getValue("y");
							//System.out.println("?x="  + valueOfX +  " ?y=" + valueOfY);

						}

						/*//iterate #2
						//result = tupleQuery.evaluate();
						List<String> bindingNames = result.getBindingNames();
						while (result.hasNext()) {
							BindingSet bindingSet = result.next();
							Value firstValue = bindingSet.getValue(bindingNames.get(0));
							Value secondValue = bindingSet.getValue(bindingNames.get(1));
							Value thirdValue = bindingSet.getValue(bindingNames.get(2));

							System.out.println("?x=" + firstValue + ", ?p=" + secondValue + ", ?y=" + thirdValue);
						}*/

						/*//iterate #3
						SPARQLResultsXMLWriter sparqlWriter = new SPARQLResultsXMLWriter(System.out);
						tupleQuery.evaluate(sparqlWriter);
						*/
					}
					finally {
						result.close();
					}
				}
				catch (Exception e) {
					//handle exception
					e.printStackTrace();
				} finally {
					con.close();
				}
			}
			catch (OpenRDFException e) {
				// handle exception
				e.printStackTrace();
			}

			/*//Evaluate a query that produces an RDF graph
			try {
				RepositoryConnection con = repo.getConnection();
				try {
					GraphQueryResult graphResult = con.prepareGraphQuery(QueryLanguage.SPARQL, 
							"PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> " +
							"CONSTRUCT {_:v rdf:type rdf:Statement; rdf:Subject ?x ; rdf:Predicate ?p; rdf:Object ?y} " +
							"WHERE {?x ?p ?y . }").evaluate();
				
					while (graphResult.hasNext()) {
						Statement st = graphResult.next();
						System.out.println(st.toString());
					}
				}
				finally {
					con.close();
				}
			}
			catch (OpenRDFException e) {
				// handle exception
				e.printStackTrace();
			}*/
			
		} catch (RepositoryException e) {
			// handle exception
			e.printStackTrace();
		}
	}
}
