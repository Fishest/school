package course.labs.todomanager;

import java.util.ArrayList;
import java.util.List;

import course.labs.todomanager.ToDoItem.Status;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.CompoundButton.OnCheckedChangeListener;
import android.widget.RelativeLayout;
import android.widget.TextView;

public class ToDoListAdapter extends BaseAdapter {

	// List of ToDoItems
	private final List<ToDoItem> mItems = new ArrayList<ToDoItem>();
	private final Context mContext;
	private static final String TAG = "Lab-UserInterface";

	public ToDoListAdapter(Context context) {
		mContext = context;
	}

	// Add a ToDoItem to the adapter
	// Notify observers that the data set has changed
	public void add(ToDoItem item) {
		mItems.add(item);
		notifyDataSetChanged();
	}
	
	// Clears the list adapter of all items.
	public void clear(){
		mItems.clear();
		notifyDataSetChanged();
	}

	// Returns the number of ToDoItems
	@Override
	public int getCount() {
		return mItems.size();
	}

	// Retrieve a specific ToDoItem
	@Override
	public Object getItem(int pos) {
		return mItems.get(pos);
	}

	// Get the ID for the ToDoItem
	// In this case it's just the position
	@Override
	public long getItemId(int pos) {
		return pos;
	}

	//Create a View to display the ToDoItem 
	// at specified position in mItems
	@Override
	public View getView(int position, View convertView, ViewGroup parent) {

		final ToDoItem item = (ToDoItem)getItem(position);

		LayoutInflater inflater = LayoutInflater.from(mContext);
		RelativeLayout itemLayout = (convertView == null)
				? (RelativeLayout)inflater.inflate(R.layout.todo_item, null)
			    : (RelativeLayout)convertView;

		final TextView titleView = (TextView)itemLayout.findViewById(R.id.titleView);
		titleView.setText(item.getTitle());
		
		final CheckBox statusView = (CheckBox)itemLayout.findViewById(R.id.statusCheckBox);
		statusView.setChecked(item.getStatus() == Status.DONE);
		statusView.setOnCheckedChangeListener(new OnCheckedChangeListener() {
			@Override
			public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
				log("Entered onCheckedChanged()");
				item.setStatus(isChecked ? Status.DONE : Status.NOTDONE);
			}
		});

		final TextView priorityView = (TextView)itemLayout.findViewById(R.id.priorityView);
		priorityView.setText(item.getPriority().toString());

		final TextView dateView = (TextView)itemLayout.findViewById(R.id.dateView);
		dateView.setText(ToDoItem.FORMAT.format(item.getDate()));

		return itemLayout;
	}
	
	private void log(String msg) {
		try {
			Thread.sleep(500);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		Log.i(TAG, msg);
	}

}
