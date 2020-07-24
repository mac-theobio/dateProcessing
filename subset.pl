use strict;
use 5.10.0;

my $input = $ARGV[0];

exit;

use Excel::Writer::XLSX;
 
# Create a new Excel workbook
my $workbook = Excel::Writer::XLSX->new( 'perl.xlsx' );
 
# Add a worksheet
$worksheet = $workbook->add_worksheet();
 
#  Add and define a format
$format = $workbook->add_format();
$format->set_bold();
$format->set_color( 'red' );
$format->set_align( 'center' );
 
# Write a formatted and unformatted string, row and column notation.
$col = $row = 0;
$worksheet->write( $row, $col, 'Hi Excel!', $format );
$worksheet->write( 1, $col, 'Hi Excel!' );
 
# Write a number and a formula using A1 notation
$worksheet->write( 'A3', 1.2345 );
$worksheet->write( 'A4', '=SIN(PI()/4)' );
 
$workbook->close();
