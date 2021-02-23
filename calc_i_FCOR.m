% Load data
load('test100k.mat');
load('Rmat.mat')

% Parameters
bw = 1.8e3;             % Bandwidth of interest [Hz]
L = 3.5e-3;             % Magnet inductance [H]
R = 0.25;               % Magnet resistance [Ohm]
Fs = 499.6649e6/19872;  % Sampling rate [Hz]
Gcorr = 30e-6;          % Magnet deflection gain [rad/A]
pinv_tol = 0;           % Pseudo inverse singular value threshold
nsv = 4;                % Numbe of singular values to be used
nbpm = 160;             % Number of BPMs
nhcorr = 80;            % Number of horizontal correctors

square_Rm = false;
bw_interest = false;
filter_sv = false;
voltage_response = false;

% Data fixes
Rm = mat;           % FIXME: should not exist
xy = xy_read'/1e3;  % FIXME: should not exist
xy = xy/1e9;        % Convert from nm to m

% Trim Response Matrix if it should be square
if square_Rm
    idx = [1:8:160 4:8:160 5:8:160 8:8:160];
    idx = sort([idx idx+160]);
    Rm = Rm(idx,:);
    xy = xy(:, idx);
end

% Matrix inverstion methods
if filter_sv
    [U,s,V] = svd(Rm,'econ');
    sv = diag(s);
    sv(nsv+1:end) = 0;
    Rc = V*diag(1./(sv))*U';
else
    Rc = pinv(Rm, pinv_tol);
end

%
if bw_interest
    [N, Fo, Ao, W] = firpmord([bw/1.2 bw]/(Fs/2), [1 0], [0.05, 1e-4]);
    Hd = dfilt.dffir(firpm(N, Fo, Ao, W, {20}));
    nsamples_reject = order(Hd);
    xy = filter(Hd, xy);
    xy = xy(nsamples_reject+1:end,:);
else
    nsamples_reject = 0;
end

% Reject DC component of BPM data
xy = detrend(xy, 0);

% Compute fast orbit corrector currents
Icorr = xy*Rc'/Gcorr;

% Project orbit distortions onto modal space
[Ux,~,~] = svd(Rm(1:nbpm, 1:nhcorr),'econ');
[Uy,~,~] = svd(Rm(nbpm+1:end, nhcorr+1:end),'econ');

modex = xy(:,1:nbpm)*Ux;
modey = xy(:,nbpm+1:end)*Uy;

if voltage_response
    % Inverse magnet dynamics - Voltage/Current transfer function
    invresp = tf([L R],[5*pi/Fs 1]);
    
    % Build time vector
    t = (0:size(xy,1)-1)'/Fs;
    
    % Simulate inverse magnet dynamics with current data
    Vcorr = zeros(size(Icorr));
    for i=1:size(Vcorr,2)
        Vcorr(:,i) = lsim(invresp, Icorr(:,i), t);
    end
end

% Compute FFTs
[Y_bpm,f] = fourierseries(xy(nsamples_reject+1:end,:), Fs);
Y_Icorr = fourierseries(Icorr(nsamples_reject+1:end,:), Fs);

if voltage_response
    Y_Vcorr = fourierseries(Vcorr(nsamples_reject+1:end,:), Fs);
end

% Plot results

% BPM data
figure
loglog(f, [max(Y_bpm,[],2) mean(Y_bpm,2) min(Y_bpm,[],2)]*1e6)
ylim([1e-6 50])
xlim([0 Fs/2])
grid on
xlabel('Frequency [Hz]')
ylabel('Position [\mum]')
legend('max spectrum', 'avg spectrum', 'min spectrum', 'Location', 'SouthWest')

% Current data
figure
loglog(f, [max(Y_Icorr,[],2) mean(Y_Icorr,2) min(Y_Icorr,[],2)]*1e3)
ylim([0.5e-5 5e2])
xlim([0 Fs/2])
grid on
xlabel('Frequency [Hz]')
ylabel('Current [mA]')
legend('max spectrum', 'avg spectrum', 'min spectrum', 'Location', 'SouthWest')

% Voltage data
if voltage_response
    figure
    loglog(f, [max(Y_Vcorr,[],2) mean(Y_Vcorr,2) min(Y_Vcorr,[],2)])
    %ylim([0.5e-5 5e2])
    xlim([0 Fs/2])
    grid on
    xlabel('Frequency [Hz]')
    ylabel('Voltage [V]')
    legend('max spectrum', 'avg spectrum', 'min spectrum', 'Location', 'SouthWest')
end

%% Modal data
idx=find(fx > 0 & fx < 2500);

figure;
ax(1) = subplot(121);
h = surf(fx(idx), 1:nbpm, 20*log10(Yx(idx,:))');
view(0,90);
h.EdgeColor = 'none';
axis tight
zlim_x = caxis;
ylabel('Mode number')
xlabel('Frequency [Hz]')
set(ax(1), 'XTick', 0:240:fx(end))
ax(1).XAxis.MinorTickValues = 0:60:fx(end);
set(ax(1), 'XMinorTick', 'on')
ylim([0 size(modex,2)]);

ax(2) = subplot(122);
h = surf(fy(idx), 1:nbpm, 20*log10(Yy(idx,:))');
view(0,90);
h.EdgeColor = 'none';
axis tight
zlim_y = caxis;
xlabel('Frequency [Hz]')
set(ax(2), 'XTick', 0:240:fx(end))
ax(2).XAxis.MinorTickValues = 0:60:fx(end);
set(ax(2), 'XMinorTick', 'on')
set(ax(2), 'XMinorTick', 'on')
ylim([0 size(modey,2)]);

zmin = floor(min([zlim_x zlim_y];
zmax = max([zlim_x zlim_y]);
zmin = -180;
zmax = -90;

subplot(121);
caxis([zmin zmax]);
colorbar
subplot(122);
caxis([zmin zmax]);
colorbar