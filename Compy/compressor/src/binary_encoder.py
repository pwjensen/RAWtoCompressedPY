# converts compressed files to bianry for efficient saving 
import pickle

class BinaryFileHandler:
    
    def __init__(self, code_map, shape, compressed_data):
        self.code_map = code_map  # dict that maps pixel values to Huffman codes
        self.shape = shape  # dimensions of the image for reconstruction
        self.compressed_data = compressed_data  # binary string of compressed data
        self.original_file_size = self.get_data_size(data=compressed_data)
        self.compressed_file_size = None  
    
    def __str__(self) -> str:
        if not self.compressed_file_size:
            return "No File Saved"
        
        # encode the data and return the instance variables 
        meta_data = {"Orginal File Size: " : self.original_file_size,
                     "Compressed File Size: " : self.compressed_file_size,
                     "Size Reduction: " : str(100 - self.compressed_file_size // self.original_file_size) + "%"}

        return str(meta_data)
    
    def get_data_size(self, data):
        # Calculate size in bytes for binary data
        if isinstance(data, str):  # Assuming 'data' is a binary string
            return len(data) // 8
        return len(data)


    def save_binary(self, filename):
        # convert the compressed binary string to bytes
        binary_data = int(self.compressed_data, 2).to_bytes((len(self.compressed_data) + 7) // 8, 'big')
        self.compressed_file_size = self.get_data_size(binary_data)  # Update compressed file size

        # serialize metadata including the updated compressed file size
        metadata = {
            'code_map': self.code_map,
            'shape': self.shape,
            'original_file_size': self.original_file_size,
            'compressed_file_size': self.compressed_file_size,
        }
        metadata_serialized = pickle.dumps(metadata)

        # write serialized metadata and binary data to file
        with open(filename, 'wb') as f:
            f.write(metadata_serialized)
            f.write(binary_data) 

    def load_binary(self, filename):
        with open(filename, 'rb') as f:
            metadata_serialized = f.read() # reading in metadata for reconstruction 
            metadata = pickle.loads(metadata_serialized)
            
            # update instance vars from metadata 
            self.code_map = metadata['code_map']
            self.shape = metadata['shape']
            self.original_file_size = metadata['original_file_size']
            self.compressed_file_size = metadata['compressed_file_size']

            # read the image pixel data
            binary_data = f.read()
            # bytes -> bits conversion 
            self.compressed_data = format(int.from_bytes(binary_data, 'big'), '0{}b'.format(len(binary_data)*8))


