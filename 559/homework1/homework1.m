%
% Simple program to read in an image, find the pixels with
% the highest red coloring, and draw cross-hairs the highest
$ and lowest matching columns.
%
function homework1(file)
	ey = imread(file);
	id = (ey(:,:,1) == 255);
	[x,y] = find(id == 1);
	
	subplot(1,2,1);
	imshow(ey);
	
	x = max(x);
	y = [min(y) max(y)];
    ey(x-10:x+10,y,:) = 0;
	for yi = y
		ey(x,yi-10:yi+10,:) =0;
	end

	subplot(1,2,2);
	imshow(ey);
end
