package com.example.shittleproject2;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

import com.example.shittleproject2.R;

public class MainActivity extends AppCompatActivity {
    MSSQLhandler mssqLhandler;
    String ip = "1.168.0.53:60000";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mssqLhandler = new MSSQLhandler();
        mssqLhandler.connect(ip);
        Toast.makeText(this, "Connection Success", Toast.LENGTH_LONG);
    }

    public void managerevent (View v){
        Intent i = new Intent(this, Manager.class);
        startActivity(i);
    }

    public void studentevent (View v){
        Intent i = new Intent(this, Student.class);

        startActivity(i);
    }
}