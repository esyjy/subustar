package com.subustar;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.EditText;

public class Manager extends AppCompatActivity {
    EditText editRfid;
    PillowNfcManager nfcManager;
    PillowNFCWriteHelper writeHelper;
    //public PillowNFCWriteHelper(Context context, PillowNfcManager nfcManager)
    /*phone number*/

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.manager);

        // writeHelper를 만들기 위해 nfcManager 객체 만들기
        nfcManager = new PillowNfcManager(this);
        nfcManager.onActivityCreate();
        //
        writeHelper = new PillowNFCWriteHelper(this, nfcManager);
        editRfid = (EditText)findViewById(R.id.editRfid);
        nfcManager.setOnTagWriteErrorListener(writeHelper);
        nfcManager.setOnTagWriteListener(writeHelper);
    }

    public void writeevent(View v) {
        String rfidtext = editRfid.getText().toString();
        writeHelper.writeText(rfidtext);
    }

    @Override
    protected void onResume() {
        super.onResume();
        // manager 프로세스 실행할 때 nfcManager의 onActivityResume 함수 실행
        nfcManager.onActivityResume();
    }

    @Override
    protected void onPause() {
        // manager 프로세스를 정지할 때 nfcManagerd의 onActivityPause 함수 실행
        nfcManager.onActivityPause();
        super.onPause();
    }

    @Override
    protected void onNewIntent(Intent intent) {
        // rfid 쓰기 버튼 누를 때 onCreate 대신에 onNewIntent 함수 실행
        nfcManager.onActivityNewIntent(intent);
    }
}
