package course.labs.activitylab;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.TextView;

public class ActivityTwo extends Activity {

	private static final String RESTART_KEY = "restart";
	private static final String RESUME_KEY = "resume";
	private static final String START_KEY = "start";
	private static final String CREATE_KEY = "create";

	// String for LogCat documentation
	private final static String TAG = "Lab-ActivityTwo";

	// Lifecycle counters
	private int mCreate  = 0;
	private int mRestart = 0;
	private int mStart   = 0;
	private int mResume  = 0;
 
	// Counter text views
	private TextView mTvCreate;
	private TextView mTvRestart;
	private TextView mTvStart;
	private TextView mTvResume;

	@Override
	protected void onCreate(Bundle state) {
		super.onCreate(state);
		setContentView(R.layout.activity_two);

		mTvCreate = (TextView)findViewById(R.id.create);
		mTvRestart = (TextView)findViewById(R.id.restart);
		mTvStart = (TextView)findViewById(R.id.start);
		mTvResume = (TextView)findViewById(R.id.resume);

		Button closeButton = (Button) findViewById(R.id.bClose); 
		closeButton.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View v) {
				ActivityTwo.this.finish();			}
		});

		// Check for previously saved state
		if (state != null) {
			mCreate  = state.getInt(CREATE_KEY, 0);
			mStart   = state.getInt(START_KEY, 0);
			mResume  = state.getInt(RESUME_KEY, 0);
			mRestart = state.getInt(RESTART_KEY, 0);
		}

		Log.i(TAG, "Entered the onCreate method");
		
		mCreate += 1;
		displayCounts();
	}

	@Override
	public void onStart() {
		super.onStart();
		Log.i(TAG, "Entered the onStart method");

		mStart += 1;
		displayCounts();
	}

	@Override
	public void onResume() {
		super.onResume();
		Log.i(TAG, "Entered the onResume method");

		mResume += 1;
		displayCounts();
	}

	@Override
	public void onPause() {
		super.onPause();
		Log.i(TAG, "Entered the onPause method");
	}

	@Override
	public void onStop() {
		super.onStop();
		Log.i(TAG, "Entered the onStop method");
	}

	@Override
	public void onRestart() {
		super.onRestart();
		super.onRestart();
		Log.i(TAG, "Entered the onRestart method");

		mRestart += 1;
		displayCounts();
	}

	@Override
	public void onDestroy() {
		super.onDestroy();
		Log.i(TAG, "Entered the onDestroy method");
	}

	@Override
	public void onSaveInstanceState(Bundle state) {
		state.putInt(CREATE_KEY, mCreate);
		state.putInt(START_KEY, mStart);
		state.putInt(RESUME_KEY, mResume);
		state.putInt(RESTART_KEY, mRestart);
	}

	/**
	 * Updates the displayed counters on the existing
	 * text widgets.
	 */
	public void displayCounts() {
		mTvCreate.setText("onCreate() calls: " + mCreate);
		mTvStart.setText("onStart() calls: " + mStart);
		mTvResume.setText("onResume() calls: " + mResume);
		mTvRestart.setText("onRestart() calls: " + mRestart);
	}
}
