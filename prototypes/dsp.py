#!/usr/bin/env python

from math import *

qua = ( .5 * pi )
tau = ( 2. * pi )
phi = ( 1 + sqrt(5) ) * .5
cot = lambda x: ( 1 / tan(x) )
exp = lambda x: ( e ** x )

def mul(seq):
	res = 1
	for n in seq:
		res *= n
	return res

# N is wavelength

hamming = lambda N,n: (cos(pi * n / N) + 1) / 2
wave = lambda N,n: e ** (1j * tau * n / N)
hamming_wave = lambda N,n: hamming(N, n) * wave(N, n)
wavelet = lambda N: [ hamming_wave(N, n) for n in range(-N, N+1) ]
window_length = lambda N: 2 * N + 1
power = lambda N: sum( hamming_wave(N, n).real * wave(N,n).real for n in range(-N, N+1) )
#power = lambda N: sum( hamming_wave(N, n).real * wave(N,n).real for n in range(-N, N+1) )



assert window_length(3) == len(wavelet(3))
#assert power(3) == len(wavelet(3))


class FilterBank:
	def __init__(self, count, wavelength=lambda b: b+2):
		#self.wavelength = wavelength
		self.count = count

		self.wavelength = wavelength

		self.wavelengths = [ wavelength(b) for b in range(count) ]
		self.window_length = max( window_length(l) for l in self.wavelengths )

		self.wavelets = [ wavelet(l) for l in self.wavelengths ]
		self.powers = [ 1/power(l) for l in self.wavelengths ]

		self.buffer = [ complex() for b in range(self.window_length) ]
		self.center_offset = ( self.window_length - 1 ) >>  1

		self.spectrum = [ complex() for _ in range(count) ]

		print('FilterBank')
		print('  count:', self.count)
		print('  window_length:', self.window_length)
		print('  center_offset:', self.center_offset)
		print('  wavelengths:', self.center_offset)


	def __call__(self, sample):
		buffer = self.buffer
		buffer.pop(0)
		buffer.append(sample)

		center_offset = self.center_offset
		wavelengths = self.wavelengths
		wavelets = self.wavelets
		powers = self.powers
		spectrum = self.spectrum

		out = .0
		for b in range(self.count):
			wavelet = wavelets[b]
			wavelength = wavelengths[b]
			offset = center_offset - wavelength

			acc = complex()
			for n, c in enumerate(wavelet):
				acc += buffer[offset + n] * c


			acc = acc * powers[b]
			#spectrum[b] = acc

			# DISTORT TYPE A
			spectrum[b] = acc + acc ** 3 *  e ** (1j * 2 * pi)  * tau
					#   source   distort   phase correction   drive

			# ^3
			# DISTORT TYPE B
			#spectrum[b] = acc + acc ** 3 + acc ** 5 + acc ** 7
					#   source   distort   phase correction   drive

			out += spectrum[b] / wavelengths[b]
			#out += spectrum[b]

		return out # + out ** 3 * e ** (1j * pi)
		#return sum(spectrum) / self.count


class PhasorBank:
	"""
		oscillator = e^(2i*pi*phase+velocity*t)*amplitude

	"""
	def __init__(self, num_oscillators):
		self.num_oscillators = num_oscillators
		self.phases = [ .0 for _ in range(num_oscillators) ]
		self.amplitudes = [ .0 for _ in range(num_oscillators) ]
		self.velocities = [ pi for _ in range(num_oscillators) ]

	def __call__(self):
		phases = self.phases
		amplitudes = self.amplitudes
		velocities = self.velocities

		out = complex()
		for n in range(self.num_oscillators):
			phase = phases[n]
			out += amplitudes[n] * e ** (1j * phase)
			phases[n] = phase + velocities[n]

		return out


	def real(self):
		phases = self.phases
		amplitudes = self.amplitudes
		velocities = self.velocities

		out = complex()
		for n in range(self.num_oscillators):
			phase = phases[n]
			out += amplitudes[n] * cos(phase)
			phases[n] = phase + velocities[n]

		return out
