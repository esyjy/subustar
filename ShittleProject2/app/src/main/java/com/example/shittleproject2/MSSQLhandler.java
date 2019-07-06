package com.example.shittleproject2;

import android.os.StrictMode;
import android.util.Log;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class MSSQLhandler {
    String classs = "net.sourceforge.jtds.jdbc.Driver";
    /* db : databse, username, password, conn : connection */
    String db = "subustar";
    String username = "cit";
    String password = "citcitcit";
    Connection conn;
    public Connection connect(String ip) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
        // connURL : 서버 접속시 필요한 ip주소, db 이름, 사용자 이름, 비밀번호
        String ConnURL = "jdbc:jtds:sqlserver://" + ip + ";" +
                "databaseName=" + db + ";user=" + username +
                ";password=" + password + ";loginTimeout=1";
        try {
            Class.forName(classs);
            DriverManager.setLoginTimeout(1);
            // 연결을 한다
            conn = DriverManager.getConnection(ConnURL);
        } catch (SQLException e) {
            Log.e("MSSQLhandler % connect ", e.getMessage()+" SQLException");
        } catch (ClassNotFoundException e) {
            Log.e("MSSQLhandler % connect ", e.getMessage()+" ClassNotFoundException");
        } catch (Exception e) {
            Log.e("MSSQLhandler % connect ", e.getMessage()+" Exception");
        }
        return conn;
    }
}
