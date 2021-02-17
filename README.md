# Python scripts to calculate correctors' current spectra from Beam Position Monitor readings

## Dependencies

* python3
* pyepics

```bash
    pip3 install pyepics --user
```

## Examples

### Read 10 ADC samples from BPMs present in 'bpmlist.pickle' file

```bash
    ./calc_i_corr.py 10 'ADC'
```

### Read 10 ADC samples from BPMs present in 'bpmlist.pickle' file

```bash
    ./calc_i_corr.py 10 'TbT'
```
