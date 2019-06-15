package com.subustar;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
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
