import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders Transcribe button", () => {
  render(<App />);
  const uploadButton = screen.getByText(/Transcribe/i);
  expect(uploadButton).toBeInTheDocument();
});

test("renders Search button", () => {
  render(<App />);
  const searchButton = screen.getByText(/Search/i);
  expect(searchButton).toBeInTheDocument();
});

test("renders Display All list", async () => {
  render(<App />);
  const displayAllButton = screen.getByText(/Display All/i);
  expect(displayAllButton).toBeInTheDocument();
});
