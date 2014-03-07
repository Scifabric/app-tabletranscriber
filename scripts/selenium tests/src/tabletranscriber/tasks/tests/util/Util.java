package tabletranscriber.tasks.tests.util;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

import tabletranscriber.tasks.tests.setup.delete_tasks.deleteTasksType1;

public class Util {
	public static List<Integer> searchAppIDsInTask() {
		Connection con = null;
        Statement st = null;
        ResultSet rs = null;

        String url = "jdbc:postgresql://localhost/pybossa";
        String user = "postgres";
        String password = "postgres";
        
        List<Integer> app_ids = new LinkedList<Integer>();
        
        try {
            con = DriverManager.getConnection(url, user, password);
            st = con.createStatement();
            rs = st.executeQuery("SELECT * FROM task");
            
            rs.next();
            
            int app_id = Integer.parseInt(rs.getString(3));
            app_ids.add(app_id);
            
            while(rs.next()) {
            	if(!app_ids.contains(Integer.parseInt(rs.getString(3)))) {
            		app_ids.add(Integer.parseInt(rs.getString(3)));
            	}
            }
            
            Collections.sort(app_ids);
            
        } catch (SQLException ex) {
            Logger lgr = Logger.getLogger(deleteTasksType1.class.getName());
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
        
        return app_ids;
	}
	
	public static List<Integer> searchAppIDsInTaskRun() {
		Connection con = null;
        Statement st = null;
        ResultSet rs = null;

        String url = "jdbc:postgresql://localhost/pybossa";
        String user = "postgres";
        String password = "postgres";
        
        List<Integer> app_ids = new LinkedList<Integer>();
        
        try {
            con = DriverManager.getConnection(url, user, password);
            st = con.createStatement();
            rs = st.executeQuery("SELECT * FROM task_run");
            
            rs.next();
            
            int app_id = Integer.parseInt(rs.getString(3));
            app_ids.add(app_id);
            
            while(rs.next()) {
            	if(!app_ids.contains(Integer.parseInt(rs.getString(3)))) {
            		app_ids.add(Integer.parseInt(rs.getString(3)));
            	}
            }
            
            Collections.sort(app_ids);
            
        } catch (SQLException ex) {
            Logger lgr = Logger.getLogger(deleteTasksType1.class.getName());
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
        
        return app_ids;
	}
}
