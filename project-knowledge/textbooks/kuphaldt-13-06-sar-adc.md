[Skip to main content](https://workforce.libretexts.org/Bookshelves/Electronics_Technology/Electric_Circuits_IV_-_Digital_Circuitry_(Kuphaldt)/13%3A_Digital-Analog_Conversion/13.06%3A_Successive_Approximation_ADC#elm-main-content "Press enter to skip to the main content")

One method of addressing the digital ramp ADC’s shortcomings is the so-called _successive-approximation_ ADC. The only change in this design is a very special counter circuit known as a _successive-approximation register_. Instead of counting up in binary sequence, this register counts by trying all values of bits starting with the most-significant bit and finishing at the least-significant bit. Throughout the count process, the register monitors the comparator’s output to see if the binary count is less than or greater than the analog signal input, adjusting the bit values accordingly. The way the register counts is identical to the “trial-and-fit” method of decimal-to-binary conversion, whereby different values of bits are tried from MSB to LSB to get a binary number that equals the original decimal number. The advantage to this counting strategy is much faster results: the DAC output converges on the analog signal input in much larger steps than with the 0-to-full count sequence of a regular counter.

Without showing the inner workings of the successive-approximation register (SAR), the circuit looks like this:

![04262.png](https://workforce.libretexts.org/@api/deki/files/3478/04262.png?revision=1)

It should be noted that the SAR is generally capable of outputting the binary number in _serial_ (one bit at a time) format, thus eliminating the need for a shift register. Plotted over time, the operation of a successive-approximation ADC looks like this:

![04263.png](https://workforce.libretexts.org/@api/deki/files/3479/04263.png?revision=1)

Note how the updates for this ADC occur at regular intervals, unlike the digital ramp ADC circuit.

×![LibreTexts Logo](https://cdn.libretexts.net/Icons/full_logo.png)

## Support Center

How can we help you today?

- Contact Support (opens in new tab)
- Search the Insight Knowledge Base (opens in new tab)
- Check System Status (opens in new tab)

Highlights hidden

Hypothesis

![Hypothesis](https://hypothes.is/organizations/__default__/logo)Public

Sign up

/

Log in

## Annotations

AnnotationsPage Notes

There are no annotations in this group.

Create one by selecting some text and clicking the  button.

Annotate

Highlight

contentsreadabilityresourcestools

☰ [13.5: Digital Ramp ADC](https://workforce.libretexts.org/Bookshelves/Electronics_Technology/Electric_Circuits_IV_-_Digital_Circuitry_(Kuphaldt)/13%3A_Digital-Analog_Conversion/13.05%3A_Digital_Ramp_ADC)

13.5: Digital Ramp ADC

 [13.7: Tracking ADC](https://workforce.libretexts.org/Bookshelves/Electronics_Technology/Electric_Circuits_IV_-_Digital_Circuitry_(Kuphaldt)/13%3A_Digital-Analog_Conversion/13.07%3A_Tracking_ADC)

13.7: Tracking ADC

Complete your gift to make an impact