package com.example.shittleproject2;


import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ImageView;
import android.widget.Toast;

/**
 * Helper for writing tags. Creates a dialog while waiting for the tag, and displays error messages with a toast
 */
public class PillowNFCWriteHelper implements PillowNfcManager.TagWriteErrorListener, PillowNfcManager.TagWriteListener{
	AlertDialog dialog;
	PillowNfcManager nfcManager;
	Context context;
	int dialogViewId = R.layout.dialog;
	
	public PillowNFCWriteHelper(Context context, PillowNfcManager nfcManager) {
		this.context = context;
		this.nfcManager = nfcManager;
	}
	
	/**
	 * Write the given text to a tag.
	 * @param text
	 */
	public void writeText(String text){
		dialog = createWaitingDialog();
		dialog.show();
		nfcManager.writeText(text);
	}
	
	public void setDialogViewId(int dialogViewId) {
		this.dialogViewId = dialogViewId;
	}

	@Override
	public void onTagWritten() {
		dialog.dismiss();
		Toast.makeText(context, R.string.msg, Toast.LENGTH_LONG).show();;
	}

	@Override
	public void onTagWriteError(PillowNFCWriteException exception) {
		dialog.dismiss();
		//TODO translate exeptions
		Toast.makeText(context, exception.getType().toString(), Toast.LENGTH_LONG).show();
	}
	
	/**
	 * Creates a dialog while waiting for the tag
	 * @return
	 */
	public AlertDialog createWaitingDialog(){
		LayoutInflater inflater = LayoutInflater.from(context);
		View view = inflater.inflate(dialogViewId, null, false);
		ImageView image = new ImageView(context);
		image.setImageResource(R.drawable.ic_launcher_background);
		AlertDialog.Builder builder = new AlertDialog.Builder(context);
		builder.setTitle(R.string.wait)
		.setView(view)
		.setNegativeButton(R.string.cancel, new DialogInterface.OnClickListener() {
           public void onClick(DialogInterface dialog, int id) {
        	   nfcManager.undoWriteText();
           }
       });
		return builder.create();
	}
	


}
