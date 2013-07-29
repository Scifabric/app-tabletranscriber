package tabletranscriber.tasks.tests.setup.delete_tasks;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

import tabletranscriber.tasks.tests.util.Util;

public class deleteTasksType3 {

    public static void main(String[] args) {

        Connection con = null;
        Statement st = null;
        ResultSet rs = null;

        String url = "jdbc:postgresql://localhost/pybossa";
        String user = "postgres";
        String password = "postgres";

        try {
            con = DriverManager.getConnection(url, user, password);
            st = con.createStatement();
            
            int type3;
            List<Integer> listAppIds = Util.searchAppIDsInTask();
            if(listAppIds.size() >= 3) {
            	type3 = listAppIds.get(2);
            }
            else {
            	System.out.println("don't exists tasks type 3");
            	return;
            }
            
            System.out.println("type3AppID = " + type3);
            
            st.execute("DELETE FROM task WHERE app_id = " + type3);
            
            System.out.println("deleted tasks type 3");

        } catch (SQLException ex) {
            Logger lgr = Logger.getLogger(deleteTasksType3.class.getName());
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
                Logger lgr = Logger.getLogger(deleteTasksType1.class.getName());
                lgr.log(Level.WARNING, ex.getMessage(), ex);
            }
        }
    }
}