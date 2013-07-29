package tabletranscriber.tasks.tests.setup.delete_tasks_runs;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

import tabletranscriber.tasks.tests.util.Util;

public class deleteTaskRunsType1 {

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
            
            int type1;
            List<Integer> listAppIds = Util.searchAppIDsInTaskRun();
            if(listAppIds.size() >= 1) {
            	type1 = listAppIds.get(0);
            }
            else {
            	System.out.println("don't exists task runs type 1");
            	return;
            }
            
            System.out.println("type1AppID = " + type1);
            
            st.execute("DELETE FROM task_run WHERE app_id = " + type1);
            
            System.out.println("deleted task_runs type 1");

        } catch (SQLException ex) {
            Logger lgr = Logger.getLogger(deleteTaskRunsType1.class.getName());
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
                Logger lgr = Logger.getLogger(deleteTaskRunsType1.class.getName());
                lgr.log(Level.WARNING, ex.getMessage(), ex);
            }
        }
    }
}