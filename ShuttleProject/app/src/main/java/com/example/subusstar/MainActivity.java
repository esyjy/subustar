package com.example.subusstar;

import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class MainActivity extends AppCompatActivity {
    Button button;
    TextView textview;

    String server = "1.168.0.53:60000";
    String db = "subustar";
    String db_connect_string = "jdbc:jtds:sqlserver://" + server + ";databaseName=" + db + ";";
    String db_userid = "cit";
    String db_password = "citcitcit";

    public Connection connect() {
        Connection conn = null;
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
        try {
            Class.forName("net.sourceforge.jtds.jdbc.Driver");
            conn = DriverManager.getConnection(
                    db_connect_string, db_userid, db_password);
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        } catch (SQLException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return conn;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        button = (Button)findViewById(R.id.button);
        textview = (TextView) findViewById(R.id.textview);
    }

    public void connect_event(View v) {
        Connection conn = connect();
        if (conn == null) {
            textview.setText("연결을 실패했습니다");
        }
        else {
            textview.setText("연결을 성공했습니다");
        }
    }
}