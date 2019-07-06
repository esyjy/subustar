package com.subustar;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
<<<<<<< HEAD

public class MainActivity extends AppCompatActivity {
=======
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {
    MSSQLhandler mssqLhandler;
    String ip = "1.168.0.53";
>>>>>>> a8843813f87e987400bd9ff00f24e64d4056169c

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
<<<<<<< HEAD
=======
        mssqLhandler = new MSSQLhandler();
        mssqLhandler.connect(ip);
        Toast.makeText(this, "Connection Success", Toast.LENGTH_LONG);
>>>>>>> a8843813f87e987400bd9ff00f24e64d4056169c
    }

    public void managerevent (View v){
        Intent i = new Intent(this, Manager.class);
        startActivity(i);
    }

    public void studentevent (View v){
        Intent i = new Intent(this, Student.class);

        startActivity(i);
}
<<<<<<< HEAD
}
=======
}
>>>>>>> a8843813f87e987400bd9ff00f24e64d4056169c
