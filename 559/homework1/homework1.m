%
% Simple program to read in an image, apply a pre determined
% red eye threshold, and subtract the pixels that match from
% the red color color portion.
%
function homework1(file);
    ey = imread(file);
    o(:,:,1) = ey(:,:,1) >= 110 & ey(:,:,1) < 255;
    o(:,:,2) = ey(:,:,2) >=   0 & ey(:,:,2) <  45;
    o(:,:,3) = ey(:,:,3) >=   0 & ey(:,:,3) <  70;
    z = o(:,:,1) & o(:,:,2) & o(:,:,3);
    
    subplot(1,3,1);
    imshow(ey);
    
    subplot(1,3,2);
    imshow(z);
    
    ey(:,:,1) = ey(:,:,1) - uint8(z).*ey(:,:,1);
    subplot(1,3,3);
    imshow(ey);
end
