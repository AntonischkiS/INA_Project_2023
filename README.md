# INA_Project_2023
In this project we created graphs about the voting beheavior in the german Bundestag for every legislature period from 1949 until today. The nodes are the parlamentarians and edge weights between the nodes is a measure of the similarity in the voting beheaviour of the parlamentarians. We created to graphs for exh legislator method. In One of the Graphs ignored votes in the edge weight calculations where both of the parlamentarians where missing and in the other one we included it in the similarity calculation. 
We used data from [abgeordnetenwatch.de](https://www.abgeordnetenwatch.de/) for the legislature periods starting after 2005 and the data from https://dataverse.harvard.edu/dataverse/btvote for the legislatur periods until 2005.

The Visualizations of the graphs in a png format created with the force atlas algorithm from gephi are located in the folder visualizations.

The created graphs saved as gexf files and in a pajek format for all legislature period of the Bundestag can be viewed at src/graphs/Bundestag or at src/graphs/Bundestag_only_Attendance (Here, all no show votes are excluded). The gexf files can be opened with gephi or other software to create your own Visualizations.

If you want to run the code yourself you need the following info:

To create the pajek format for the data from dataverse.harvard.edu you need download the voting_behavior_V2_19492021.dta file first and put into the project at src\data\BTVote\voting_behavior_V2_19492021.dta. Then run the notebook src/create_network_btvote.ipynb and asign the ep variable the number of the legislature period for which you want to create the graph and set the abscence DISREGARD_ABSENCE Variable to True or false wether you want to ignore the noshow options or not.

To create the pajek format for the abgeordnetenwatch data you need to first execute the download_data.py file with the first year of the legislator period as argument. Then you need to run the python file create_Network.py with the first year of the legislator period you want to create as an argument as an argument. if you want to ignore the noshow option in the graph creation you need to replace the generating_edges() method in the create_graph_file_from_legislature_data() method on line 188 with the generating_edges2() method and also replace the BUNDESTAG_GRAPH_PATH variable in the main method with BUNDESTAG_GRAPH_PATH_V2.

To create gexf files from the pajek format you need to run the pajek_to_gexf.py file with the with the first year of the legislator period as argument. Here you can also replace the BUNDESTAG_GRAPH_PATH variable in the main method with BUNDESTAG_GRAPH_PATH_V2 depending on which Graph you want to create.
The Visualizations of the graphs created with the force atlas algorithm from gephi are located in the folder visualizations.


