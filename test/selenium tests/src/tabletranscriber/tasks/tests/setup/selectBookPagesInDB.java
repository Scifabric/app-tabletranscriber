package tabletranscriber.tasks.tests.setup;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;

public class selectBookPagesInDB {

    public static void run() {

        Connection con = null;
        Statement st = null;
        ResultSet rs = null;

    
        String url = "jdbc:postgresql://localhost/pybossa";
        String user = "postgres";
        String password = "postgres";

        try {
            con = DriverManager.getConnection(url, user, password);
            st = con.createStatement();
            rs = st.executeQuery("SELECT * FROM task");
            
            rs.next();
            int firstID = Integer.parseInt(rs.getString(1));
            
            // de acordo com paginas do anuario
            int arrayOfOriginalIDs[] = {64,65,181,183,11,12,13,14,15}; 
            ArrayList<Integer> arrayOfFinalIDs = new ArrayList<Integer>();
            
            for(int i = 0; i < arrayOfOriginalIDs.length; i++) {
            	arrayOfFinalIDs.add(firstID + arrayOfOriginalIDs[i]);
            	System.out.println("final IDs: " + (firstID + arrayOfOriginalIDs[i] - 1));
            }
            
            String arrayFinalIDsToString = "(" + arrayOfFinalIDs.get(0);
            for(int j = 1; j < arrayOfFinalIDs.size(); j++) {
            	arrayFinalIDsToString += ", " + arrayOfFinalIDs.get(j);
            }
            arrayFinalIDsToString += ")";
            
            System.out.println("arrayFinalIDsToString: " + arrayFinalIDsToString);
            
            st.execute("DELETE FROM task WHERE id NOT IN " + arrayFinalIDsToString);

        } catch (SQLException ex) {
            Logger lgr = Logger.getLogger(selectBookPagesInDB.class.getName());
            lgr.log(Level.SEVERE, ex.getMessage(), ex);

        } finally {
            try {
                if (rs != null) {
                    rs.close();
                }
                if (st != null) {
                    st.close();
                }
                if (con != null) {
                    con.close();
                }

            } catch (SQLException ex) {
                Logger lgr = Logger.getLogger(selectBookPagesInDB.class.getName());
                lgr.log(Level.WARNING, ex.getMessage(), ex);
            }
        }
    }
}