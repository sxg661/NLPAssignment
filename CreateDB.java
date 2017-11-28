package Database;

import java.sql.Connection;
import java.util.Random;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Scanner;

public class CreateDB {
	
	private int[] cid = new int[2000];
	private int[] jid = new int[200];
	private int[] gid = new int[200];
	private int[] hid = new int[200];
	private int[] crackersaleprice = new int[2000];
	private int[] crackerquantity = new int[2000];
	private int[] royalties = new int[200];
	private int[] giftprice = new int[200];
	private int[] hatprice = new int[200];
	private String[] names = new String[2000];
	private String[] crackerqueries = new String[2000];
	private String[] jokequeries = new String[200];
	private String[] giftqueries = new String[200];
	private String[] hatqueries = new String[200];
	private String[] dropqueries = {"DROP TABLE Cracker", "DROP TABLE Joke", "DROP TABLE Gift", "DROP TABLE Hat"};
	private String[] jokes = new String[200];
	private String[] gifts = new String[200];
	private String[] hats = new String[200];
	Random randomGenerator = new Random();
	int j = 0;
	int k = 0;
	int b = 0;
	int o = 0;
	int z = 0;
	int u = 0;
	int ind3 = 0;
	int ind6 = 0;
	int ind9 = 0;
	
	public CreateDB() {
		for (int i = 0; i < cid.length;i++) {
			cid[i] = i;
			//System.out.println("Cid array contains: " + cid[i]);
		}
		
		for (int m = 0; m < names.length; m++) {
			names[m] = "Christmas cracker " + m;
			//System.out.println("Names array contains: " + names[m]);
		}
		
		for (int n = 0; n < jid.length;n++) {
			jid[n] = n;
			//System.out.println("Jid array contains: " + jid[n]);
		}
		
		for (int s = 0; s < gid.length;s++) {
			gid[s] = s;
			//System.out.println("Gid array contains: " + gid[s]);
		}
		
		for (int p = 0; p < hid.length;p++) {
			hid[p] = p;
			//System.out.println("Hid array contains: " + hid[p]);
		}
		
		for (int e = 0; e < crackersaleprice.length;e++) {
			crackersaleprice[e] = randomGenerator.nextInt(5)+1;
			//System.out.println(crackersaleprice[e]);
		}
		
		for (int g = 0; g < crackerquantity.length; g++) {
			crackerquantity[g] = randomGenerator.nextInt(600)+1;
			//System.out.println(crackerquantity[g]);
		}
		
		for (int v = 0; v < royalties.length; v++) {
			royalties[v] = randomGenerator.nextInt(10)+1;
			//System.out.println(royalties[v]);
		}
		
		jokes[0] = "Moses had the first table that could connect to the cloud.";
		jokes[1] = "A doctor tells a woman that she cannot touch anything alcoholic, so she got a divorce.";
		jokes[2] = "Why was six scared of seven? Because seven ate nine.";
		jokes[3] = "Did you hear about the guy whose left side was cut off? He is all right now.";
		jokes[4] = "Why is it that your nose runs but your feet smell?";
		jokes[5] = "If you ever get cold, just stand in the corner of a room for a while, they are normally around 90 degrees";
		jokes[6] = "I am great at multitasking. I can waste time, be unproductive, and procrastinate all at once.";
		jokes[7] = "I never forget a face, but in your case I would love to make an exception.";
		jokes[8] = "What do you call a fat psychic? A four chin teller.";
		jokes[9] = "I used to like my neighbours until they put a password on their wi-fi.";
		for (int q = 10; q < jokes.length; q++) {
			jokes[q] = "Joke " + q;
		}
		
		gifts[0] = "A ball-point pen.";
		gifts[1] = "A wooden spoon.";
		gifts[2] = "Cufflinks.";
		gifts[3] = "A bottle opener.";
		gifts[4] = "Stickers.";
		gifts[5] = "Honey dippers.";
		gifts[6] = "Colouring pencils.";
		gifts[7] = "A star cookie cutter.";
		gifts[8] = "Chocolates.";
		gifts[9] = "A tea strainer.";
		for (int q = 10; q < gifts.length; q++) {
			gifts[q] = "Gift " + q;
		}
		
		for (int ind4 = 0; ind4 < giftprice.length;ind4++) {
			giftprice[ind4] = randomGenerator.nextInt(3)+1;
			//System.out.println(giftprice[ind4]);
		}
		
		hats[0] = "A red paper hat";
		hats[1] = "A blue paper hat.";
		hats[2] = "A purple paper hat.";
		hats[3] = "A green paper hat.";
		hats[4] = "A yellow paper hat";
		hats[5] = "An orange paper hat.";
		hats[6] = "A white paper hat.";
		hats[7] = "A pink paper hat.";
		hats[8] = "A grey paper hat.";
		hats[9] = "A brown paper hat.";
		for (int q = 10; q < hats.length; q++) {
			hats[q] = "Hat " + q;
		}
		
		for (int ind10 = 0; ind10 < hatprice.length;ind10++) {
			hatprice[ind10] = randomGenerator.nextInt(3)+1;
			//System.out.println(hatprice[ind10]);
		}
		
	}
	

	 public Connection connectToDB(String url, String username, String pass) {
	        System.out.println("Attempting to connect to mod-intro-databases server...");

	        try {
	            Class.forName("org.postgresql.Driver");
	        } catch (ClassNotFoundException ex) {
	            System.out.println("Driver not found.");
	            System.exit(1);
	        }

	        System.out.println("PostgreSQL driver registered.");

	        Connection conn = null;
	        try {
	            conn = DriverManager.getConnection(url, username, pass);
	        } catch (SQLException ex) {
	            System.out.println("Connection could not be established.");
	            System.exit(1);
	        }

	        if (conn != null) {
	            System.out.println("Database accessed!");
	        } else {
	            System.out.println("Failed to make connection.");
	            System.exit(1);
	        }
	        
	       
	        return conn;
	 }
	        
	        
	 public void createTables(Connection conn) {
	        // +++ Create primary and foreign keys for each table
	        System.out.println("Creating tables...");
	        try {
	        	String createCracker = "CREATE TABLE Cracker (" + 
	        			"	cid		INTEGER, " + 
	        			"	name	CHAR(200)	NOT NULL, " +
	        			"	jid		INTEGER		NOT NULL UNIQUE, " + 
	        			"	gid		INTEGER		NOT NULL UNIQUE, " + 
	        			"	hid		INTEGER		NOT NULL UNIQUE, " + 
	        			"	saleprice	INTEGER		NOT NULL, " +
	        			"	quantity	INTEGER		NOT NULL, "  +
	        			" 	PRIMARY KEY (cid)" +
	        			"	)";
	        			
	        	String createJoke = "CREATE TABLE Joke (" + 
	        			"	jid		INTEGER, " + 
	        			"	joke	VARCHAR(300), " +
	        			"	royalty	INTEGER		NOT NULL, " +
	        			" 	PRIMARY KEY (jid), " +
	        			" 	FOREIGN KEY(jid) REFERENCES Cracker(jid) " +
	        			" 	)";
	        	
	        	String createGift = "CREATE TABLE Gift (" + 
	        			"	gid				INTEGER, " +
	        			"	giftdescription	VARCHAR(300), " +
	        			"	price			INTEGER		NOT NULL, " +
	        			" 	PRIMARY KEY (gid), " +
	        			"	FOREIGN KEY(gid) REFERENCES Cracker(gid) " +
	        			"	)";
	        			
	        	String createHat = "CREATE TABLE Hat (" + 
	        			"	hid				INTEGER, " + 
	        			"	hatdescription	VARCHAR(100), " +
	        			"	price			INTEGER		NOT NULL, " +
	        			" 	PRIMARY KEY(hid) " +
	        			"	FOREIGN KEY (hid) REFERENCES Cracker(hid) " +
	        			"	)";
	        			
	        	
	        	
	        	PreparedStatement cracker = conn.prepareStatement(createCracker);
	        	PreparedStatement joke = conn.prepareStatement(createJoke);
	        	PreparedStatement gift = conn.prepareStatement(createGift);
	        	PreparedStatement hat = conn.prepareStatement(createHat);
	        	cracker.executeUpdate();
	        	joke.executeUpdate();
	        	gift.executeUpdate();
	        	hat.executeUpdate();	
	        }
	        catch(SQLException sqlE) { 
	        	System.out.println(sqlE);
	        }
	 }
	        
	  public void makeQueries()	{
	        	while (j < crackerqueries.length && k < names.length && b < jid.length) {
	        		crackerqueries[j] = "INSERT INTO Cracker VALUES (" + cid[j] + ", " + "'" + names[k] + "'" + ", " + jid[b] + ", " + gid[b] + ", " + hid[b] + ", " + crackersaleprice[j] + ", " + crackerquantity[j] + ")";
        			//System.out.println("List of Cracker queries: " + crackerqueries[j]);
        			j++;
        			if (k == names.length-1) {
        				k = 0;
        			}
        			else {
        				k++;
        			}
        			if (b == jid.length-1) {
        				b = 0;
        			}
        			else {
        				b++;
        			}
	        	}
	        	
	        	// making the joke insert queries
	        	while (o < jokequeries.length && z < jokes.length) {
	        		jokequeries[o] = "INSERT INTO Joke VALUES (" + jid[o] + ", " + "'" + jokes[z] + "' " + ", " + royalties[z] + ")";
	        		//System.out.println("List of Joke queries: " + jokequeries[o]);
	        		o++;
	        		if (z == jokes.length-1) {
	        			z = 0;
	        		}
	        		else {
	        			z++;
	        		}
	        	}
	        	
	        	// making the gift insert queries
	        	while (u < giftqueries.length && ind3 < gifts.length) {
	        		giftqueries[u] = "INSERT INTO Gift VALUES (" + gid[u] + ", " + "'" + gifts[ind3] + "'" + ", " + giftprice[ind3] + ")";
	        		//System.out.println("List of Gift queries: " + giftqueries[u]);
	        		u++;
	        		if (ind3 == gifts.length-1) {
	        			ind3 = 0;
	        		}
	        		else {
	        			ind3++;
	        		}
	        	}
	        	
	        	// making the hat insert queries
	        	while (ind6 < hatqueries.length && ind9 < hats.length) {
	        		hatqueries[ind6] = "INSERT INTO Hat VALUES (" + hid[ind6] + ", " + "'" + hats[ind9] + "'" + ", " + hatprice[ind9] + ")";
	        		//System.out.println("List of Hat queries: " + hatqueries[ind6]);
	        		ind6++;
	        		if (ind9 == hats.length-1) {
	        			ind9 = 0;
	        		}
	        		else {
	        			ind9++;
	        		}
	        	}
	  }
	        	
	  public void populateDB(Connection conn) {
		  try {
	        	// populating the cracker table
	        	for (int l = 0; l < cid.length; l++) {
	        		String string = crackerqueries[l];
	        		PreparedStatement insert = conn.prepareStatement(string);
	        		insert.addBatch();
	        		insert.executeBatch();
	        	}
	        	
	        	System.out.println("Table Cracker has been successfully created!");
	        	
	        	// populating the joke table
	        	for (int x = 0; x < jid.length; x++) {
	        		String string1 = jokequeries[x];
	        		PreparedStatement insert1 = conn.prepareStatement(string1);
	        		insert1.addBatch();
	        		insert1.executeBatch();
	        	}
	        
	        	System.out.println("Table Joke has been successfully created!");
	        	
	        	// populating the gift table
	        	for (int ind2 = 0; ind2 < gid.length; ind2++) {
	        		String string2 = giftqueries[ind2];
	        		PreparedStatement insert2 = conn.prepareStatement(string2);
	        		insert2.addBatch();
	        		insert2.executeBatch();
	        	}
	        	
	        	System.out.println("Table Gift has been successfully created!");
	        	
	        	// populating the hat table
	        	for (int ind8 = 0; ind8 < hid.length; ind8++) {
	        		String string3 = hatqueries[ind8];
	        		PreparedStatement insert3 = conn.prepareStatement(string3);
	        		insert3.addBatch();
	        		insert3.executeBatch();
	        	}
	        	
	        	System.out.println("Table Hat has been successfully created!");
	        	System.out.println("The tables have been successfully created!");
		  }
		  catch(SQLException sqlE) {
			  System.out.println(sqlE);
		  }
	  }
	        	
	  
	  public void interfaceDB(Connection conn) {
	        	try {
		  		// GUI begins here!!!
	        	// Giving Cracker ID
	        	Scanner scanner = new Scanner(System.in);
	        	System.out.println("What is the ID of the cracker you'd like to inspect?");
	        	int scancid = scanner.nextInt();
	        	//scanner.close();
	        	System.out.println("Printing: Cracker ID, Cracker name, Description of corresponding gift, Corresponding joke, Description of corresponding hat, Cracker unit saleprice, Cracker unit cost price, Cracker quantity sold, Cracker profit");
	        	PreparedStatement scancidquery = conn.prepareStatement("SELECT Cracker.cid, Cracker.name, Cracker.saleprice, Cracker.quantity, Joke.joke, Gift.giftdescription, Hat.hatdescription FROM Cracker, Joke, Gift, Hat WHERE cid = " + scancid + " AND Cracker.jid = Joke.jid AND Cracker.gid = Gift.gid AND Cracker.hid = Hat.hid");
	        	ResultSet rs = scancidquery.executeQuery();
	        	
	        	
	        	// SELECT Cracker.cid, Cracker.name, Cracker.saleprice, Cracker.quantity, Joke.joke, Gift.giftdescription, Hat.hatdescription FROM Cracker, Joke, Gift, Hat WHERE Cracker.cid = scancid AND Cracker.jid = Joke.jid AND Cracker.gid = Gift.gid AND Cracker.hid = Hat.hid
	        	// above query lacks the "cracker unit cost price" and "crack net profit" -- will optimise later
	        	int querycid = 0;
	        	String querycrackername = null;
	        	String querygiftdescr = null;
	        	String queryjoke = null;
	        	String queryhatdescr = null;
	        	
	        	while(rs.next()) {
	        		querycid = rs.getInt("cid");
	        		querycrackername = rs.getString("name");
	        		querygiftdescr = rs.getString("giftdescription");
	        		queryjoke = rs.getString("joke");
	        		queryhatdescr = rs.getString("hatdescription");
	        		System.out.println("Cracker ID: " + querycid);
	        		System.out.println("Cracker name: " + querycrackername);
	        		System.out.println("Joke: " + queryjoke);
	        		System.out.println("Gift: " + querygiftdescr);
	        		System.out.println("Hat: " + queryhatdescr);
	        	}
	        	
	        	// Giving Joke ID
	        	// initialise scanner again here and do scanner.close() when method is created
	        	System.out.println("What is the ID of the joke you'd like to inspect?");
	        	int scanjid = scanner.nextInt();
	        	//scanner.close();
	        	System.out.println("Printing: Joke ID, joke, royalty paid to creator of joke, number of times this joke was used, total royalty payment to creator of joke");
	        	PreparedStatement scanjidquery = conn.prepareStatement("SELECT jid, joke, royalty FROM Joke WHERE jid = " + scanjid);
	        	ResultSet rs1 = scanjidquery.executeQuery();
	        	
	        	// SELECT jid, joke, royalty FROM Joke WHERE jid = scanjid
	        	// above query lacks "number of times joke was used" and "total royalty payment to creator of joke" -- will optimise later
	        	int queryjid = 0;
	        	String queryjoke1 = null;
	        	int queryroyalty = 0;
	        	
	        	while (rs1.next()) {
	        		queryjid = rs1.getInt("jid");
	        		queryjoke1 = rs1.getString("joke");
	        		queryroyalty = rs1.getInt("royalty");
	        		System.out.println("Joke ID: " + queryjid);
	        		System.out.println("Joke: " + queryjoke1);
	        		System.out.println("Royalty due to creator of joke: " + queryroyalty);
	        	}
	        	
	        	// Inserting new cracker into database
	        	// MIND THE CONSTRAINTS GODDAMNIT
	        	// initialise scanner again her and do scanner.close() when method is created
	        	System.out.println("Please fill in the following information in order to insert a new cracker.");
	        	System.out.println("What's the ID of the cracker you would like to insert to the database?");
	        	int newcid = scanner.nextInt();
	        	System.out.println("What's the name of the cracker you would like to insert to the database?");
	        	String newname = scanner.next();
	        	System.out.println("What's the ID of the joke that corresponds to the cracker you would like to insert to the database?");
	        	int newjid = scanner.nextInt();
	        	System.out.println("What's the ID of the gift that corresponds to the cracker you would like to insert to the database?");
	        	int newgid = scanner.nextInt();
	        	System.out.println("What's the ID of the hat that corresponds to the cracker you would like to insert to the database?");
	        	int newhid = scanner.nextInt();
	        	System.out.println("What's the saleprice of the cracker you would like to insert to the database?");
	        	int newsaleprice = scanner.nextInt();
	        	System.out.println("How many of these crackers are available?");
	        	int newquantity = scanner.nextInt();
	        	scanner.close();
	        	if (newcid > 2000 && newjid > 120 && newgid > 120 && newhid > 120) {
	        	PreparedStatement newinsert = conn.prepareStatement("INSERT INTO Cracker VALUES (" + newcid + ", " + "'" + newname + "'" + ", " + newjid + ", " + newgid + ", " + newhid + ", " + newsaleprice + ", " + newquantity + ")");	        	
	        	newinsert.executeUpdate();
	        	}
	        	else {
	        		System.out.println("Wrong input, please check that your cracker ID is larger than 2000, and joke ID, gift ID and hat ID over 120");
	        	}
	 }
	  catch(SQLException sqlE) {
		  System.out.println(sqlE);
	  }
	  }
	        	// run program again to verify creation? I know it works.
	        	
	        //Now, just tidy up by closing connection
	  
		 // problem with conn - watch your methods
		 private void dropTables(Connection conn) {
	     	try {
	     	 System.out.println("Dropping pre-existent tables...");
			 for (int ind12 = 0; ind12 < dropqueries.length; ind12++) {
	     		String drop = dropqueries[ind12];
	     		PreparedStatement dropinsert = conn.prepareStatement(drop);
	     		dropinsert.addBatch();
	     		dropinsert.executeBatch();
	     	}
	     	}
	     	catch(SQLException sqlE) {
	     		System.out.println("The tables don't exist for them to be dropped!");
	     	}
		 }
	  
	  
	  public void closeConnection(Connection conn) {
		  try {
          conn.close();
          System.out.println("Connection closed!");
      } catch (SQLException ex) {
          ex.printStackTrace();
      }
	  }
	      





	    

	    // Main method to connect to database on the module server.
	    public static void main(String[] args) {

	        String username = "axc591";
	        String password = "FomgQ2Wix2";
	        String database = "";
	        String URL = "jdbc:postgresql://mod-intro-databases.cs.bham.ac.uk/" + database;
	        // Need it fully qualified if connecting via vpn

	        CreateDB db = new CreateDB();
	        long startTime = System.nanoTime();
	        Connection conn = db.connectToDB(URL, username, password);
	        db.dropTables(conn);
	        db.createTables(conn);
	        db.makeQueries();
	        db.populateDB(conn);
	        db.interfaceDB(conn);
	        db.closeConnection(conn);
	        long endTime = System.nanoTime();
	        long duration = (endTime - startTime);
	        System.out.println("Duration of program is: " + duration + " nanoseconds.");
	        // under normal circumstances it takes about 80 seconds for the program to properly run
	        // at home computer, but it might change based on the method arrangement
	        // it runs in 20-30 
	        
	    }
	
	
}